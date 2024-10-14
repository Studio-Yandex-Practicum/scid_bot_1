from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from api.api_managers import (
    manager_login_with_tg_id,
    set_order_to_work
)
from keyboards.manager import (
    MANAGER_MAIN_MENU,
    OrderCallback,
    START_MANAGER_WORK,
    generate_order_keyboard,
    generate_order_work_keyboard
)
from utils.manager_content import (
    generate_order_text,
    get_all_orders_for_manager,
    show_message
)
from utils.manager_state import ManagerState


router = Router()


@router.message(Command("manager"))
async def manager_start(message: types.Message, state: FSMContext):
    """Обработка команды /manager"""
    await state.clear()
    bot_message = await message.answer(
            text="Авторизация...",
            reply_markup=None
        )
    user_info = await manager_login_with_tg_id(message.from_user.id)
    if user_info["is_manager"]:
        await state.update_data(
            jwt=f"{user_info['token_type']} {user_info['jwt']}",
            current_user_id=message.from_user.id
        )
        await state.set_state(ManagerState.authorized)
        await bot_message.edit_text(
            text="Авторизация успешна"
        )
        await bot_message.edit_reply_markup(
            reply_markup=START_MANAGER_WORK
        )
    else:
        await bot_message.edit_text(
            text="Вход недоступен, так как Вы не являетесь менеджером"
        )


@router.callback_query(F.data=="go_to_start")
async def manager_go_to_main_menu(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Возврат к главному меню"""
    await state.set_state(ManagerState.authorized)
    await manager_authorized(callback, state)


@router.callback_query(
    F.data=="None" or
    OrderCallback.filter(F.current_order == -1)
)
async def manager_cancel_flashing(callback: types.CallbackQuery):
    """Убирает раздражающее мигание"""
    await callback.answer()


@router.callback_query(
    ManagerState.authorized,
    F.data=="manager_start_work"
)
async def manager_authorized(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Начало работы менеджера"""
    text = (
        "<b>Что Вы хотите увидеть?</b>\n\n"
        "<b>Новые заявки</b> - заявки, которые еще не приняты в работу\n"
        "<b>Заявки в работе</b> - заявки, которые Вы взяли в работу"
    )
    await show_message(
        text=text,
        reply_keyboard=MANAGER_MAIN_MENU,
        state=state,
        new_state=None,
        message=callback.message
    )


@router.callback_query(F.data=="managers_end_work")
async def manager_cancel_work(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Завершение работы менеджера"""
    await callback.message.delete()
    await state.clear()


@router.callback_query(ManagerState.authorized, F.data=="new_order")
async def manager_new_orders_show(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Отображение новых заявок"""
    data = await state.get_data()
    orders = await get_all_orders_for_manager(
        jwt=data['jwt'],
        in_progress=False
    )
    orders_len = len(orders)
    if orders_len == 0:
        text = "Новых заявок нет"
    else:
        text = await generate_order_text(orders[0])

    await show_message(
        text=text,
        reply_keyboard=await generate_order_keyboard(orders_len=len(orders)),
        state=state,
        new_state=ManagerState.new_orders,
        message=callback.message,
        state_update_data={'orders': orders}
    )

@router.callback_query(
    ManagerState.new_orders,
    OrderCallback.filter(F.current_order >= 0),
    OrderCallback.filter(F.to_work == False)
)
async def manager_current_orders_show(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: OrderCallback
):
    """Отображение конкретной новой заявки"""
    data = await state.get_data()
    await show_message(
        text=await generate_order_text(
            data['orders'][callback_data.current_order]
        ),
        reply_keyboard=await generate_order_keyboard(
            page=callback_data.current_order,
            orders_len=len(data['orders'])
        ),
        state=state,
        new_state=None,
        message=callback.message
    )


@router.callback_query(
    ManagerState.new_orders,
    OrderCallback.filter(F.to_work == True)
)
async def manager_current_orders_show(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: OrderCallback
):
    """Взятие заявки в работу"""
    data = await state.get_data()
    await state.set_state(ManagerState.order_in_progress)
    response = await set_order_to_work(
        jwt=data['jwt'],
        order_id=data['orders'][callback_data.current_order]['id'],
        manager_tg_id=data['current_user_id']
    )
    if 'detail' in response:
        await state.set_state(ManagerState.authorized)
        await callback.message.answer(
            text=response['detail'],
            reply_markup=MANAGER_MAIN_MENU
        )
        return
    await show_message(
        text=await generate_order_text(
            data['orders'][callback_data.current_order],
            preview=False
        ),
        reply_keyboard=await generate_order_work_keyboard(
            callback.message.from_user.id,
            order_id=data['orders'][callback_data.current_order]['id']
        ),
        state=state,
        new_state=None,
        message=callback.message
    )
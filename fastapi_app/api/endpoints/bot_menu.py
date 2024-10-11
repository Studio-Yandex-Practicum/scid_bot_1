from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.bot_menu_validators import (
    check_button_exist,
    check_button_file_exist,
    check_button_image_file_exist,
    check_button_is_main_menu,
)
from core.db import get_async_session
from core.users import current_superuser
from crud.bot_menu import bot_menu_crud, bot_menu_files_crud
from models.bot_menu import MenuButton
from schemas.bot_menu import (
    MenuButtonChildrenResponse,
    MenuButtonCreate,
    MenuButtonFileCreate,
    MenuButtonFileResponse,
    MenuButtonResponse,
    MenuButtonUpdate
)
from services.bot_menu import delete_image_file_if_exist
from services.files import delete_file, save_file

router = APIRouter(prefix='/bot_menu', tags=['bot_menu'])


@router.get(
    '/get-main-menu-button',
    response_model=MenuButtonResponse,
    summary='Возвращает первую (базовую) кнопку',
    description=('Изначальная кнопка, к которой привязываются все осталньые'),
)
async def get_main_menu_button(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[MenuButton]:
    return await bot_menu_crud.get_main_menu_button(session=session)


@router.get(
    '/{button_id}/get-content',
    response_model=MenuButtonResponse,
    summary='Возвращает контент, который должна отображать кнопка',
    description=('Возвращает: текст, изображение, файлы, ссылку'),
)
async def get_button_content(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Optional[MenuButton]:
    return await check_button_exist(
        button_id=button_id,
        session=session,
    )


@router.get(
    '/{button_id}/get-image-file',
    summary='Возвращает файл изображения кнопки',
    description=('Передаёт файл изображения, указанный для кнопки'),
)
async def get_button_image_file(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_button_image_file_exist(button_id=button_id, session=session)
    return FileResponse(
        path=await check_button_image_file_exist(button_id, session)
    )


@router.get(
    '/{button_id}/get-child-buttons',
    response_model=list[MenuButtonChildrenResponse],
    summary='Возвращает список дочерних кнопок, для текущей',
    description=('Возвращает: id кнопки, родителя и её название'),
)
async def get_button_children(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[MenuButton]:
    await check_button_exist(
        button_id=button_id,
        session=session,
    )
    return await bot_menu_crud.get_children_button(
        button_id=button_id,
        session=session,
    )


@router.post(
    '/{button_id}/add-child-button',
    response_model=MenuButtonResponse,
    dependencies=[Depends(current_superuser)],
    summary='Добавляет кнопку в базу данных',
    description=('Добавляет кнопку к родителю, как дочернюю'),
)
async def create_new_bot_menu_button(
    button_id: int,
    label: str = Form(...),
    content_text: Optional[str] = Form(None),
    content_link: Optional[str] = Form(None),
    content_image: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    await check_button_exist(
        button_id=button_id,
        session=session,
    )
    if content_image is not None:
        image_path = await save_file(content_image)
    else:
        image_path = None
    return await bot_menu_crud.create(
        obj_in=MenuButtonCreate(
            label=label,
            content_text=content_text,
            content_link=content_link,
            content_image=image_path,
        ),
        parent_id=button_id,
        session=session,
    )


@router.patch(
    '/{button_id}/change_parent',
    response_model=MenuButtonResponse,
    dependencies=[Depends(current_superuser)],
    summary='Изменяет родителя кнопки',
)
async def change_parent(
    button_id: int,
    new_parent_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    return await bot_menu_crud.change_parent_button(
        menu_button=await check_button_is_main_menu(
            button_id=button_id, session=session
        ),
        new_parent_id=new_parent_id,
        session=session,
    )


@router.patch(
    '/{button_id}',
    response_model=MenuButtonResponse,
    dependencies=[Depends(current_superuser)],
    summary='Обновляет кнопку меню',
    description=(
        'Не обновляет поле родителя, обновляет только поля:'
        'название, контент текст, контент изображение (путь до файла), '
        'контент ссылка'
    ),
)
async def update_bot_menu_button(
    button_id: int,
    label: Optional[str] = Form(None),
    content_text: Optional[str] = Form(None),
    content_link: Optional[str] = Form(None),
    content_image: Optional[UploadFile] = File(None),
    remove_content_image: Optional[bool] = Form(None),
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    existing_button = await check_button_exist(
        button_id=button_id, session=session
    )
    if content_image is not None:
        await delete_image_file_if_exist(existing_button)
        image_path = await save_file(content_image)
    else:
        image_path = existing_button.content_image
        if remove_content_image:
            image_path = None

    update_data = MenuButtonUpdate(
        label=label if label else existing_button.label,
        content_text=content_text
        if content_text
        else existing_button.content_text,
        content_link=content_link
        if content_link
        else existing_button.content_link,
        content_image=image_path,
    )
    return await bot_menu_crud.update(
        db_obj=existing_button,
        obj_in=update_data,
        session=session,
    )


@router.delete(
    '/{button_id}',
    response_model=MenuButtonResponse,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет кнопку меню',
    description=('Безвозвратно удаляет кнопку меню И ВСЕ ДОЧЕРНИЕ.'),
)
async def delete_bot_menu_button(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    button = await check_button_is_main_menu(
        button_id=button_id,
        session=session,
    )
    children = await bot_menu_crud.get_children_button(
        button_id=button.id,
        session=session,
    )
    files = await bot_menu_files_crud.get_all_files_info(
        button_id=button_id,
        session=session,
    )
    await delete_file(button.content_image)
    for file in files:
        await delete_file(file.file_path)
        await bot_menu_files_crud.delete(file, session)
    for child in children:
        await delete_bot_menu_button(child.id, session)
    return await bot_menu_crud.delete(
        db_obj=button,
        session=session,
    )


@router.post(
    '/{button_id}/files',
    response_model=list[MenuButtonFileResponse],
    dependencies=[Depends(current_superuser)],
    summary='Добавляет файлы к кнопке',
    description=('Добавляет файлы, как вложение, для возможности скачивания'),
)
async def add_files_to_button(
    button_id: int,
    files: list[UploadFile] = File(...),
    session: AsyncSession = Depends(get_async_session),
):
    await check_button_exist(
        button_id=button_id,
        session=session,
    )

    file_responses = []
    for file in files:
        file_path = await save_file(file)
        db_file = await bot_menu_files_crud.create(
            obj_in=MenuButtonFileCreate(
                file_path=file_path,
                file_type=file.content_type,
                button_id=button_id,
            ),
            session=session,
        )
        file_responses.append(db_file)

    return file_responses


@router.get(
    '/{button_id}/files',
    response_model=list[MenuButtonFileResponse],
    summary='Возвращает информацию о прикреплённых к кнопке файлах',
)
async def get_bot_button_files_info(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    await check_button_exist(
        button_id=button_id,
        session=session,
    )
    return await bot_menu_files_crud.get_all_files_info(
        button_id=button_id,
        session=session,
    )


@router.delete(
    '/{button_id}/files',
    response_model=MenuButtonFileResponse,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет файл из кнопки',
    description=('Безвозвратно удаляет файл из вложений кнопки и с сервера'),
)
async def delete_bot_menu_button_file(
    button_id: int,
    file_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    await check_button_exist(
        button_id=button_id,
        session=session,
    )
    file = await check_button_file_exist(file_id=file_id, session=session)
    await delete_file(file.file_path)
    return await bot_menu_files_crud.delete(
        db_obj=file,
        session=session,
    )

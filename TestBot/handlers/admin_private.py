from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from kbds.reply import get_keyboard

admin_router = Router()

ADMIN_KB = get_keyboard(
    'Добавить игрока',
    'Изменить игрока',
    'Удалить игрока',
    'Я так, просто посмотреть зашел',
    placeholder='Выберите действие',
    sizes=(2, 1, 1),
)

@admin_router.message(Command('admin'))
async def add_product(message: types.Message):
    await message.answer('Что хотите сделать?', reply_markup=ADMIN_KB)


@admin_router.message(F.text == 'Я так, просто посмотреть зашел')
async def starring_at_product(message: types.Message):
    await message.answer('ОК, вот наш состав')


@admin_router.message(F.text == 'Изменить игрока')
async def change_product(message: types.Message):
    await message.answer('Ок, вот наш состав')


@admin_router.message(F.text == 'Удалить игрока')
async def delete_product(message: types.Message):
    await message.answer('Выберите товар(ы) для удаления')



class AddProduct(StatesGroup):
    #Шаги состояний
    name = State() #инициалы
    club = State() #клуб
    price = State() #цена на трансферном рынке
    image = State() #его фотка

    texts = {
        'AddProduct:name':'Введите инициалы заново:',
        'AddProduct:club':'Введите клуб заново:',
        'AddProduct:price':'Введите стоимость заново:',
        'AddProduct:image':'Этот стейт последний, поэтому...',
    }


@admin_router.message(StateFilter(None), F.text == 'Добавить игрока')
async def add_player(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите инициалы игрока", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)

@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет, или введите инициалы игрока или напишите "отмена')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step

@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введители команду игрока")
    await state.set_state(AddProduct.club)

@admin_router.message(AddProduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст инициала игрока")

@admin_router.message(AddProduct.club, F.text)
async def add_club(message: types.Message, state: FSMContext):
    await state.update_data(club=message.text)
    await message.answer("Введите стоимость игрока")
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.club)
async def add_club2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст клуба игрока")

@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите фотку игрока")
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите стоимость игрока")

@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Игрок добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

@admin_router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, отправьте фото игрока")

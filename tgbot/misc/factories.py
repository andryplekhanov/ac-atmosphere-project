from aiogram.utils.callback_data import CallbackData

for_cat = CallbackData('category', 'category_id')
for_prod = CallbackData('product', 'product_id', 'prev_cat')
for_back = CallbackData('back', 'prev_cat', 'section')
for_order = CallbackData('order', 'prod_id')

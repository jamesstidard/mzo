import maya

import mz


@mz.command()
@mz.arguments.name()
@mz.arguments.amount()
@mz.options.sort_code()
@mz.options.account_number()
@mz.options.message()
@mz.options.on_datetime()
@mz.options.daily_frequency_flag()
@mz.options.weekly_frequency_flag()
@mz.options.monthly_frequency_flag()
@mz.options.yearly_frequency_flag()
@mz.options.user_defined_frequency()
async def pay(name, amount, sort_code, account_number, message, on, every):
    print('paying:', name)
    print('amount:', amount)
    print('sort_code:', sort_code)
    print('account_number:', account_number)
    print('message:', message)
    print('on:', maya.when(on).slang_date())
    print('every:', every)

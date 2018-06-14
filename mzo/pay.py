import maya

import mzo.utils.authentication


@mzo.command(short_help='Schedule one-off or reoccurring payment.')
@mzo.arguments.name()
@mzo.arguments.amount()
@mzo.options.sort_code()
@mzo.options.account_number()
@mzo.options.message()
@mzo.options.on_datetime()
@mzo.options.daily_frequency_flag()
@mzo.options.weekly_frequency_flag()
@mzo.options.monthly_frequency_flag()
@mzo.options.yearly_frequency_flag()
@mzo.options.user_defined_frequency()
@mzo.utils.authentication.authenticated
async def pay(name, amount, sort_code, account_number, message, on, every):
    print('paying:', name)
    print('amount:', amount)
    print('sort_code:', sort_code)
    print('account_number:', account_number)
    print('message:', message)
    print('on:', maya.when(on).slang_date())
    print('every:', every)

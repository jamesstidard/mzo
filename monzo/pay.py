import maya

import monzo
import monzo.utils.authentication


@monzo.command(short_help='Schedule one-off or reoccurring payment.')
@monzo.arguments.name()
@monzo.arguments.amount()
@monzo.options.sort_code()
@monzo.options.account_number()
@monzo.options.message()
@monzo.options.on_datetime()
@monzo.options.daily_frequency_flag()
@monzo.options.weekly_frequency_flag()
@monzo.options.monthly_frequency_flag()
@monzo.options.yearly_frequency_flag()
@monzo.options.user_defined_frequency()
@monzo.utils.authentication.authenticated
async def pay(name, amount, sort_code, account_number, message, on, every):
    print('paying:', name)
    print('amount:', amount)
    print('sort_code:', sort_code)
    print('account_number:', account_number)
    print('message:', message)
    print('on:', maya.when(on).slang_date())
    print('every:', every)

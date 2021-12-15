import connect_dataset as cd


def check_user(cust_id, password):
    session = cd.connect_dataset()
    chk_password = session.execute('select password from bank_dataset.cust where cust_id=%s', (cust_id,)).one().password
    if password == str(chk_password):
        session.shutdown()
        return True
    else:
        session.shutdown()
        return False


def return_credit_details(cust_id):
    session = cd.connect_dataset()
    record = session.execute('select credit_balance,due from bank_dataset.credit where cust_id=%s', (cust_id,)).one()
    balance, due = record.credit_balance, record.due
    session.shutdown()
    return balance,due


""""def pay_due(cust_id, paid_due):
    session = cd.connect_dataset()
    due = session.execute('select due from bank_dataset.credit where cust_id=%s', (cust_id,)).one().due
    due = due - paid_due
    session.execute('update bank_dataset.credit set due=%s where cust_id=%s', (due, cust_id))
    session.execute("commit")
    session.shutdown()
    return due
"""

def check_balance(cust_id):
    session = cd.connect_dataset()
    balance = session.execute('select balance from bank_dataset.debit where cust_id=%s', (cust_id,)).one().balance
    session.shutdown()
    return balance


def credit_use(cust_id, req_credit):
    session = cd.connect_dataset()
    credit_balance = session.execute('select credit_balance from bank_dataset.credit where cust_id=%s',
                                     (cust_id,)).one().credit_balance
    if credit_balance >= req_credit:
        credit_balance = credit_balance - req_credit
        debit_balance = session.execute('select debit_balance from bank_dataset.debit where cust_id=%s', (cust_id,)).balance
        debit_balance += req_credit
        session.execute('update bank_dataset.debit set balance=%s where cust_id=%s', (debit_balance, cust_id))
        session.execute('update bank_dataset.credit set credit_balance=%s where cust_id=%s', (credit_balance, cust_id))
        session.shutdown()
        return credit_balance
    else:
        session.shutdown()
        return False


def acc_transfer(cust_id, bef_cust_id, debit_amount):
    session = cd.connect_dataset()
    balance = session.execute('select balance from bank_dataset.debit where cust_id=%s', (cust_id,)).one().balance
    check = session.execute('select count(1) from bank_dataset.cust where cust_id=%s', (bef_cust_id,)).one().count
    if check > 0:
        if balance >= debit_amount:
            balance -= debit_amount
            bef_balance = session.execute('select balance from bank_dataset.debit where cust_id=%s', (bef_cust_id,)).one().balance
            bef_balance += debit_amount
            session.execute('update bank_dataset.debit set balance=%s where cust_id=%s', (balance, cust_id))
            session.execute('update bank_dataset.debit set balance=%s where cust_id=%s', (bef_balance, bef_cust_id))
            session.shutdown()
            return -1
        else:
            session.shutdown()
            return 0
    else:
        session.shutdown()
        return 1

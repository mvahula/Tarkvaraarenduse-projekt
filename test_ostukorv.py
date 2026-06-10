from ostukorv import arvuta_summa

def test_arvuta_summa():
    assert arvuta_summa([2, 3, 5]) == 10

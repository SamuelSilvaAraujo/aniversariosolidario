from nucleo.models import Doacao
from pagseguro.models import Transaction
from pagseguro.signals import notificacao_recebida


def pagseguro_notificacao_recebida(sender, transaction, **kwargs):
    transaction_instance = Transaction.objects.get(code=transaction.get('code'))
    doacao = Doacao.objects.get(id=int(transaction.reference))
    doacao.pagamento.status = transaction_instance.status
    doacao.pagamento.save(update_fields=['status'])

notificacao_recebida.connect(pagseguro_notificacao_recebida)
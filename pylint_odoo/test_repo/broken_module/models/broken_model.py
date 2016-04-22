# coding: utf-8

from openerp import fields, models, _


def function_no_method():
    pass


class TestModel(models.Model):
    _name = 'test.model'

    _columns = {}  # deprecated columns
    _defaults = {}  # deprecated defaults

    name = fields.Char(
        _(u"Näme"),  # Don't need translate
        help=u"My hëlp",
        required=False)

    # Imported openerp.fields use Char (Upper case)
    other_field = fields.char(
        name=_("Other field"),
        copy=True,
    )

    other_field2 = fields.char(
        'Other Field2',
        copy=True,
    )

    ids = ["parent_id_1", "parent_id_2"]

    def sql_method(self, ids):
        # This is the better way and should not be detected
        self._cr.execute('SELECT DISTINCT child_id '
                         'FROM account_account_consol_rel '
                         'WHERE parent_id IN %s',
                         (tuple(ids),))

    def sql_injection_method(self, ids):
        # SQL injection, bad way
        self.env.cr.execute('SELECT DISTINCT child_id '
                            'FROM account_account_consol_rel '
                            'WHERE parent_id IN %s'
                            % (tuple(ids),))

    def sql_injection_method2(self, ids):
        # SQL injection, bad way too
        self.env.cr.execute('SELECT DISTINCT child_id '
                            'FROM account_account_consol_rel '
                            'WHERE parent_id IN %s'
                            % (tuple(ids),))

    def sql_injection_method3(self, ids):
        # This cr.execute should not be detected
        self._cr.execute2('SELECT DISTINCT child_id '
                          'FROM account_account_consol_rel '
                          'WHERE parent_id IN %s',
                          (tuple(ids),))

    def sql_injection_method4(self, ids):
        # SQL injection, using self._cr.execute directly.
        self._cr.execute('SELECT DISTINCT child_id '
                         'FROM account_account_consol_rel '
                         'WHERE parent_id IN %s'
                         % (tuple(ids),))

    def sql_injection_method5(self, ids):
        var = "select * from table where id in %s"
        values = ([1, 2, 3, ], )
        self._cr.execute(var % values)  # sql injection too

    def my_method1(self, variable1):
        #  Shouldn't show error of field-argument-translate
        self.my_method2(_('hello world'))

    def my_method2(self, variable2):
        return variable2

    def my_method3(self, variable2):
        self.env.cr.commit()  # Dangerous use of commit
        return variable2

    def my_method4(self, variable2):
        self.env.cr2.commit()  # This should not be detected
        return variable2

    def my_method5(self, variable2):
        self.env.cr.commit2()  # This should not be detected
        return variable2

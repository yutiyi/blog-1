from wtforms.form import Form
from tornado.escape import to_unicode


class TornadoMultiDict:
    def __init__(self, formdata):
        self.formdata = formdata

    def __iter__(self):
        return self.formdata

    def __contains__(self, name):
        return name in self.formdata

    def __getitem__(self, name):
        return str(self.formdata[name])

    def getlist(self, name):
        return [to_unicode(item) for item in self.formdata.get(name)]


class BaseForm(Form):
    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        if formdata is not None:
            formdata = TornadoMultiDict(formdata)
        super().__init__(formdata, obj, prefix, data, meta, **kwargs)

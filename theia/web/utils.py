from theia.web.forms import MetadataForm
from theia.web.models.metadata import MetaData

from flask_wtf import FlaskForm

def marshal(obj) -> object | None:
    """
    Validates and marshals a form into a
    provided model object
    """

    print(dir(obj))
    print(obj.__dict__)

def test_marshal():
    
    marshal(MetaData())

test_marshal()


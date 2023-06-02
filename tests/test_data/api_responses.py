import json as j

POPULATED_TEMPLATES = j.loads(j.dumps({'templates': ['with_empty_label', 'with_nonexistent_parent_element', 'without_label_field',
                                                     'minimum_valid', 'valid_parent_and_children', 'empty', 'without_id_field',
                                                     'parent_and_child_with_the_same_id', 'with_empty_id', 'without_label_with_link']}))
UPLOAD_SUCCESS = 'Template successfully uploaded. tmpl_id={0}'
INSTALL_SUCCESS = 'Template with tmpl_id={0} successfully installed!'
WRONG_DEPENDENCY = j.loads(j.dumps(
    {'message': "Dependency form {'id': 'with_nonexistent_parent_element', 'label': 'With parent element that does not exist', 'depends': 'ID_which_does_not_exist'} is not presented in template"}))
INCORRECT_FILETYPE = j.loads(
    j.dumps({'message': "Allowed file types are {'yaml', 'yml'}"}))
NO_FILE_IN_THE_REQUEST = 'No file part in the request'
NO_TEMPLATE_FOUND = 'No template with tmpl_id={0} found!'
INVALID_TEMPLATE_FORMAT = 'Invalid template format!'
NO_ID_FIELD = 'No "id" field in {\'label\': \'element without id\'}'
LINK_WITHOUT_LABEL_NOT_ALLOWED = j.loads(j.dumps(
    {'message': "Links without labels are not allowed. Error occurred in {'id': 'without_label_with_link', 'link': 'https://google.com'}"}))

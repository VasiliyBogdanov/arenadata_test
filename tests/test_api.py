import allure
import pytest

from conftest import (TEMPLATES, format_wrong_yaml_message, get_resp_message,
                      get_templates_message)

from .test_data.api_responses import (INCORRECT_FILETYPE, INSTALL_SUCCESS,
                                      INVALID_TEMPLATE_FORMAT,
                                      LINK_WITHOUT_LABEL_NOT_ALLOWED,
                                      NO_FILE_IN_THE_REQUEST, NO_ID_FIELD,
                                      NO_TEMPLATE_FOUND, POPULATED_TEMPLATES,
                                      UPLOAD_SUCCESS, WRONG_DEPENDENCY)

# GET


@allure.suite("Templates API")
class TestTemplatesAPI():

    def test_empty(self, api):
        """Template collection should be empty, before we upload any templated with valid extensions"""
        resp = api.get_templates()
        status_code = resp.status_code
        resp_message = get_templates_message(resp)

        assert resp_message == []
        assert status_code == 200

    def test_populated(self, api, populate_with_test_data):
        """All templated with valid templates should've been uploaded and available through GET request"""
        resp = api.get_templates()
        status_code = resp.status_code

        assert resp.json() == POPULATED_TEMPLATES
        assert status_code == 200

    # POST

    @pytest.mark.parametrize("filepath",
                             [pytest.param(TEMPLATES.minimum_valid,
                                           id=TEMPLATES.minimum_valid.name),
                              pytest.param(TEMPLATES.without_id_field,
                                           id=TEMPLATES.without_id_field.name,
                                           marks=pytest.mark.xfail(reason="Loaded file without ID field, which is mandatory. (Should we check file structure on upload?)")),
                              pytest.param(TEMPLATES.without_label_field,
                                           id=TEMPLATES.without_label_field.name,
                                           marks=pytest.mark.xfail(reason="Loaded file without Label field, which is mandatory. (Should we check file structure on upload?)")),
                              pytest.param(TEMPLATES.empty, id=TEMPLATES.empty.name, marks=pytest.mark.xfail(
                                  reason="Loaded valid .yaml, but empty file (Should we check file structure on upload?)"))
                              ])
    def test_post_template(self, api, filepath):
        """Template with valid extension should be uploaded correctly"""
        tmpl_id = filepath.name
        resp = api.post_template(
            filepath.value)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == UPLOAD_SUCCESS.format(tmpl_id)
        assert status_code == 201

    def test_post_minimum_valid_template_with_tmpl_id(self, api):
        """Template with valid extension should be uploaded correctly with optional 'tmpl_id' parameter"""
        filepath = TEMPLATES.minimum_valid.value
        tmpl_id = TEMPLATES.minimum_valid.name
        resp = api.post_template(
            filepath,
            tmpl_id)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == UPLOAD_SUCCESS.format(tmpl_id)
        assert status_code == 201

    @pytest.mark.parametrize("filepath", [
        pytest.param(TEMPLATES.correct_yaml_without_extension,
                     id=TEMPLATES.correct_yaml_without_extension.name),
        pytest.param(TEMPLATES.pdf_extension, id=TEMPLATES.pdf_extension.name)
    ])
    def test_post_incorrect_filetype(self, api, filepath):
        """Template with incorrect extension should not be uploaded, error with allowed file types should be returned"""
        resp = api.post_template(filepath.value)
        status_code = resp.status_code
        text_message, formats = format_wrong_yaml_message(resp)

        assert text_message + \
            "{{{}}}".format(formats) == INCORRECT_FILETYPE.format(formats)
        assert status_code == 400

    def test_post_without_file_attribute(self, api):
        """Post request without 'file' should result in 'No file part in the request' error"""
        resp = api.post_template(TEMPLATES.minimum_valid.value, file=False)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == NO_FILE_IN_THE_REQUEST
        assert status_code == 400

    def test_post_same_file_twice(self, api):
        """Uploading template with name, that already exist, should rewrite it, not create new one"""
        for i in range(2):
            api.post_template(TEMPLATES.minimum_valid.value)

        assert len(get_templates_message(api.get_templates())) == 1,\
            "Posting the same file twice should result in rewriting, not creating new one"

    @pytest.mark.parametrize("filename", [
        pytest.param(TEMPLATES.minimum_valid, id=TEMPLATES.minimum_valid.name),
        pytest.param(TEMPLATES.valid_parent_and_children,
                     id=TEMPLATES.valid_parent_and_children.name),
        pytest.param(TEMPLATES.with_empty_label, id=TEMPLATES.with_empty_label.name, marks=pytest.mark.xfail(
            reason="Should template elements with empty label fields be processed?"))
    ])
    def test_install_correct_templates(self, api, populate_with_test_data, filename):
        """Templates with correct structure should be installed successfully"""
        tmpl_id = filename.name
        resp = api.install_template(tmpl_id)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == INSTALL_SUCCESS.format(tmpl_id)
        assert status_code == 200

    @pytest.mark.parametrize("filename", [
        pytest.param(TEMPLATES.empty, id=TEMPLATES.empty.name),
        pytest.param(TEMPLATES.without_label_field,
                     id=TEMPLATES.without_label_field.name),
        pytest.param(TEMPLATES.parent_and_child_with_the_same_id,
                     id=TEMPLATES.parent_and_child_with_the_same_id.name),
        pytest.param(TEMPLATES.with_empty_id, id=TEMPLATES.with_empty_id.name, marks=pytest.mark.xfail(
            reason="Should we be able to install template with empty id field?")),
        pytest.param(TEMPLATES.with_empty_label, id=TEMPLATES.with_empty_label.name, marks=pytest.mark.xfail(
            reason="Should we be able to install template with empty label field?"))
    ])
    def test_install_incorrect_templates(self, api, populate_with_test_data, filename):
        """Trying to install templates with incorrect structure should result in 'Invalid template format' error"""
        tmpl_id = filename.name
        resp = api.install_template(tmpl_id)
        status_code = resp.status_code

        assert get_resp_message(resp) == INVALID_TEMPLATE_FORMAT
        assert status_code == 400

    def test_install_template_without_id_field(self, api, populate_with_test_data):
        """Trying to install template with no id field should result in 'No id field' error."""
        resp = api.install_template(TEMPLATES.without_id_field.name)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == NO_ID_FIELD
        assert status_code == 400

    def test_install_template_with_dependency_which_does_not_exist(self, api, populate_with_test_data):
        """Trying to install template with wrong dependency should result in 'wrong dependency' error"""
        tmpl_id = TEMPLATES.with_nonexistent_parent_element.name
        resp = api.install_template(tmpl_id)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == WRONG_DEPENDENCY
        assert status_code == 400

    def test_install_template_without_label_with_link(self, api, populate_with_test_data):
        """Trying to install template, element of which contains link,
        but no label, should result in 'Link without label not allowed' error"""
        tmpl_id = TEMPLATES.without_label_with_link.name
        resp = api.install_template(tmpl_id)
        status_code = resp.status_code
        resp_message = get_resp_message(resp)

        assert resp_message == LINK_WITHOUT_LABEL_NOT_ALLOWED
        assert status_code == 400

    # DELETE

    def test_delete_uploaded_template(self, api):
        """Deleting template, presented in templates list, with valid 'tmpl_id', should work correctly"""
        tmpl_id = TEMPLATES.minimum_valid.name
        api.post_template(TEMPLATES.minimum_valid.value)
        resp = api.delete_template(tmpl_id)
        status_code = resp.status_code

        assert sorted(get_templates_message(api.get_templates())) == []
        assert status_code == 200

    def test_delete_nonexistent_template(self, api):
        """Trying to delete templated with 'tmpl_id', that is not present in templates list, should result in 'No template found' error"""
        tmpl_id = TEMPLATES.minimum_valid.name
        resp = api.delete_template(tmpl_id)
        resp_message = get_resp_message(resp)
        status_code = resp.status_code

        assert resp_message == NO_TEMPLATE_FOUND.format(tmpl_id)
        assert status_code == 404

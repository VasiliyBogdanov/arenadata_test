from pathlib import Path

import requests as r


class API:

    def __init__(self, url):
        self.url = url

    def get_templates(self):
        """List all currently uploaded templates."""

        endpoint = "/api/v1/templates"
        req = r.get(self.url + endpoint)
        return req

    def post_template(self, filepath, tmpl_id=None, file=True):
        """Upload your template file.
        Required: file=[file]
        Optional: data={"tmpl_id":"my_custom_id"}
        """

        endpoint = "/api/v1/templates"
        abs_path = Path.resolve(filepath)
        files = {'file': open(abs_path, "rb")}

        req = r.post(url=self.url + endpoint,
                     files=files if file else {},
                     data={"tmpl_id": tmpl_id} if tmpl_id else {}
                     )
        return req

    def delete_template(self, tmpl_id):
        """Delete previously loaded template."""

        endpoint = f"/api/v1/templates/{tmpl_id}"
        req = r.delete(url=self.url + endpoint,
                       params={"tmpl_id": tmpl_id})
        return req

    def install_template(self, tmpl_id):
        """Install previously uploaded template."""

        endpoint = f"/api/v1/templates/{tmpl_id}/install"
        req = r.post(url=self.url + endpoint,
                     params={"tmpl_id": tmpl_id})
        return req

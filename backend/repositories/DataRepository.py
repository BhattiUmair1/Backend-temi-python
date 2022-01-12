
class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    #########  afspraken  #########
    @staticmethod
    def read_all_entries():
        sql = ""  # <-- Invullen met querry eens database ok
        test_return = "De get van alle entries werkt"
        return test_return

    @staticmethod
    def read_entry_on_uid(uid_afsrpaak):
        sql = ""  # <-- Invullen met querry eens database ok
        params = [uid_afsrpaak]  # <-- Invullen met params eens database ok
        if uid_afsrpaak == "Ok":
            resp = "De entry is aaanwezig"
            return resp
        elif uid_afsrpaak == "NietOk":
            resp = "De entry is niet aanwezig"
            return resp
        else:
            resp = "Error invalid UID"
            return resp

    @staticmethod
    def add_entry(entryJson):
        sql = ""  # <-- Invullen met querry eens database ok
        params = [entryJson]  # <-- Invullen met params eens database ok
        resp = f"Add {entryJson} done"
        return resp

    @staticmethod
    def update_entry(updateInfo):
        sql = ""  # <-- Invullen met querry eens database ok
        params = [entryJson]  # <-- Invullen met params eens database ok
        resp = f"Update {updateInfo} done"
        return resp

    @staticmethod
    def delete_entry(deleteInfo):
        sql = ""  # <-- Invullen met querry eens database ok
        params = [entryJson]  # <-- Invullen met params eens database ok
        resp = f"Delete {deleteInfo} done"
        return resp

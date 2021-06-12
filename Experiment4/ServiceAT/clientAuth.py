from elg import Authentication

auth = Authentication.init('offline_access')
#auth = Authentication.init()
auth.to_json('authJSONFile')



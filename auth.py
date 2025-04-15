from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Trình duyệt sẽ mở để xác thực

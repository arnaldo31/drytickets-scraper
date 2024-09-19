import gspread
import pandas
import numpy as np
import datetime

creds = {
    "type": "service_account",
    "project_id": "crypto-messari",
    "private_key_id": "9cd2f9d784c4baaba89c4f5f8a565ac47d2b33ab",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCwQ2KpOgPnA7wv\nuBjzFYbkL8vmfuFlQ1e3j8IqG0Ikale7bWfc24E21cK4ZX1zeCbN5R4Rcb560q4L\nLTiLLvsfcZYyh+WCtdih//Jdg7LelwejNP8FemVy5eXvtaWJVLIVw7XDDLxA34dQ\nXrtTECiiT4cZ4S+m/Pt7m6h8e1f3ddrKbAjr91vq6gWlY0x5bIJwvjoc8jkcKzpj\ndQ6VBa6SHjQ2X4qUUEzxflpDh+qbgXm208VBr/sMfwtzueL+F9NmvJ3jSkF/Ahjl\nSNPuKXY6TbwqS+oaPf7mFQRsvXTJ0o7skVLqsoOEsAYd1DDV12usKZaQV35CUh/p\nmSvG9+k5AgMBAAECggEALQO4kaFIV9ojWEh6zrHDtkjimOX0aCkPoMhs/NXjSWuD\nJlGlgcjpMfjbdr4skK2xs0l9KVVUIQfm/OG6nAkOhxQ6GIOOQJhyT8UOv4UfzCrj\n/3FMY7jDadl+pH5OXUktBdPqenqpJSQw6XyX+Hma9wC6bwiMY+gdzY6OM+RILeEV\nc58YvulFxSHAwmb5voh5SEalnnC4G3dO3qOwBaMRzNmEpSs9OIDWQ4/BKCrvViyI\ntcpHgCt/d9AtiU61k1GxJzFiiJt/Pu5abmfnvQhZcLrhG9rkoO4dZ1zvbKKYUzgk\nZkw3Yt1Xk3y34S5rl42XsVOmNAeaRkIy/ZoqDTLZ9QKBgQDm5mWV3Awb5iJjj3C5\n/jigoxLWuBiHkBEQg7krjnStBaAOms1fIWBUP6mw5cBH+BM17uij8c1eqRT3HVwZ\n0j+qQKbd65erMtlmOYucUJSbWcX/kEXIfXEYP+hAmSTAuir8Eqgtu0V7jgpa5ffH\npweCn9Pf1lzckKwqhCT709IrxwKBgQDDbIdamsk85GgZcvaXuEYptg3sVTKsksuV\n7+hymV7sC2zDgegvdde3aFX1VwxlXPdvqJvdWPSWran2lI3Mz6eTPWMSlBPt+tLq\nXYNWSKzQ06WE+eVUmE61WDVw0x8+Jr5aubg8OA6DhdLI6IDqvFp7v4QNB0EvVPsu\nWCT6OgNC/wKBgAFfwZ8ArjnERtQc2Gji8GdUURpiAhNcch2NCx8NO/iDng44MZyt\nUCtwLYxV8az79vFNOKkxGS3FB9DopdGphKN4uwV7D23/YXfQQ9psSFYcVKdOrnug\n83lXeARaZPOYqATT/5g2ExXHJJyh3bWcctj+Jn6ggfD2E3A1VRsCia+lAoGACmUV\ndg5Rsfl8SA5Da6KTqNhUOUP25BMS3TDbrmzWDbw11thsH0onZUwZdmlg8WtWhgvz\n7nwy1mj6Z3FTcZeCFGTphi12Oexjl6/NsqM+/gSkA0S/nBZV6XN9tDimqsmoym6i\njCF3NCvEIIetg87tCTQQtBi0sO3WRorNvLmlPsUCgYAtSEFVqcTe6D6c6mNjyfhX\nrMJ2tR3l9q37C2k4GtXdx1LFeoNusEOyMU7GMTUL5gd7q571IW92mow5U04GmsXp\n2DfA41nVUT7sqnkVCoFt6LQDS+s/5v5KnxNZ23ZEul5Qbygfx9PQaZ/TuyaxZ6+S\nhJrcuKgiWaFyED4Lni/XsQ==\n-----END PRIVATE KEY-----\n",
    "client_email": "pythoncryptomessariaccount@crypto-messari.iam.gserviceaccount.com",
    "client_id": "112559430258363988070",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pythoncryptomessariaccount%40crypto-messari.iam.gserviceaccount.com"
}

def get_today_sheet():
    
    while True:
        try:
            gc = gspread.service_account_from_dict(creds)
            spreed_sheet_id = '1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8'
            sheet = gc.open_by_key(spreed_sheet_id)
            worksheet = sheet.worksheet('Today')
            data = worksheet.get_all_values()
            df = pandas.DataFrame(data[1:], columns=data[0])
            return df
        except gspread.exceptions.APIError:
            continue  
        
def update_yesterday_sheet():
    
    df = get_today_sheet()
    df = df.drop_duplicates()
    df = df.replace(np.NAN,'')
    
    while True:
        try:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            gc = gspread.service_account_from_dict(creds)
            spreed_sheet_id = '1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8'
            sheet = gc.open_by_key(spreed_sheet_id)
            worksheet = sheet.worksheet('Yesterday')
            worksheet.batch_clear(["A1:EZ"])
            columns = df.columns.values.tolist()
            
            body = df.values.tolist()
            save = []
            save.append(columns)
            for item in body:
                save.append(item)
            worksheet.update(values=save,range_name='A1',)
            print('Yesterday Movies Updated! ',datetime.datetime.now() , ' | total: ' + str(len(df)))
            break
        except gspread.exceptions.APIError:
            continue

if __name__ == '__main__':
    update_yesterday_sheet()
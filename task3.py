import pygame
import requests
import sys
import os

def print_image(coordinates, mashtab):
    try:
        smashtab = ','.join([str(i) for i in mashtab])
        scoordinates = ','.join([str(i) for i in coordinates])
        map_request = "http://static-maps.yandex.ru/1.x/?ll=" + scoordinates + "&spn=" + smashtab + "&l=sat"
        response = requests.get(map_request)    
        if not response:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи во временный файл:", ex)
        sys.exit(2)
    return(map_file)

koord = [37.530887, 55.703118]
dx = 2.6
dy = 1
masht = [0.002, 0.002]
#masht = [1.0, 1.0]
map_file = print_image(koord, masht) 

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
a = True
while a:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.KEYDOWN:
        pr_izm = False
        if event.key == pygame.K_PAGEUP:
            if masht[0] / 2 >= 0.001:
                masht[0] = masht[0] / 2
                masht[1] = masht[0] / 2
                pr_izm = True
            else:
                print("Увеличить масштаб больше нельзя")
              
        if event.key == pygame.K_PAGEDOWN:
            if masht[0] * 2 <= 100:
                masht[0] *= 2
                masht[1] *= 2
                pr_izm = True
            else:
                print("Уменьшить масштаб больше нельзя") 
                
        if event.key == pygame.K_LEFT:
            koord[0] -= dx * masht[0]
            pr_izm = True 

        if event.key == pygame.K_RIGHT:
            koord[0] += dx * masht[0]
            pr_izm = True   

        if event.key == pygame.K_UP:
            koord[1] += dy * masht[1]
            pr_izm = True 

        if event.key == pygame.K_DOWN:
            koord[1] -= dy * masht[1]
            pr_izm = True   
            
        if pr_izm:
            os.remove(map_file)
            map_file = print_image(koord, masht)   
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()             
        pass
pygame.quit()
os.remove(map_file)



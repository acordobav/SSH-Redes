import sys
from typing import AsyncIterable
import pygame
import subprocess
import ssh_client


red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 125, 0)
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 0, 127)
orange = (255, 128, 0)
sky = (0, 255, 255)

windowWidth = 800
windowHeight = 700

ipTextX = 25
ipTextY = 25

connectButtonX = 600
connectButtonY = 25
connectButtonWidth = 160
connectButtonHeigth = 50

fileTextX = 25
fileTextY = 150

analyzeButtonX = 600
analyzeButtonY = 150
analyzeButtonWidth = 160
analyzeButtonHeigth = 50

outputTextX = 25
outputTextY = 300


class GUI:

    def __init__(self):

        pygame.init()
        pygame.font.init()

        self.running = True

        self.gameWindow = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption("Cliente SSH")
        self.clock = pygame.time.Clock()

        self.text = pygame.font.SysFont('consolas', 25)
        self.buttonText = pygame.font.SysFont('consolas', 35)

        self.actualText = 1
        self.ipAdress = ""
        self.filePath = ""
        self.output = [""]



    def startGUI(self):

        while True:

            self.gameWindow.fill(black)

            mouse = pygame.mouse.get_pos()

            connectButtonPosX = connectButtonX <= mouse[0] <= connectButtonX + connectButtonWidth
            connectButtonPosY = connectButtonY <= mouse[1] <= connectButtonY + connectButtonHeigth
            analyzeButtonPosX = analyzeButtonX <= mouse[0] <= analyzeButtonX + analyzeButtonWidth
            analyzeButtonPosY = analyzeButtonY <= mouse[1] <= analyzeButtonY + analyzeButtonHeigth

            self.drawIpText()
            self.drawConnectButton(connectButtonPosX, connectButtonPosY)
            self.drawFileText()
            self.drawAnalyzeButton(analyzeButtonPosX, analyzeButtonPosY)
            self.drawOutputText()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    ssh_client.close()
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if connectButtonPosX and connectButtonPosY:
                        #Connect function
                        self.output = [""]
                        result = ssh_client.connect(self.ipAdress)
                        if result == 0:
                            self.output.append("Connection established!")
                        elif result == 1:
                            self.output.append("Please copy key file")
                        else:
                            self.output.append("Couldn't connect to the server")



                    elif analyzeButtonPosX and analyzeButtonPosY:
                        # File upload
                        upload = ssh_client.upload_file(self.filePath, "./text.txt")
                        if upload == 0:
                            self.output.append("File uploaded")
                        else:
                            self.output.append("Error uploading")

                        # File analysis
                        exec = ssh_client.exec_command("python3 entity_recognition.py text.txt")
                        if exec == 1:
                            self.output.append("Error analyzing file")
                        else:
                            self.output.append("Analysis completed")
                        
                        # Result download
                        download = ssh_client.download_file("./resultado.txt", "./resultado.txt")
                        if download == 1:
                            self.output.append("Error downloading the file")
                        else:    
                            self.output.append("File downloaded")
                            self.output.append("Result stored in resultado.txt")

                        

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_TAB:
                        if self.actualText == 2:
                            self.actualText = 1
                        else:
                            self.actualText += 1

                    self.handleNumericKeyboard(event)
                    self.handleLetterKeyboard(event)

            pygame.display.update()
            self.clock.tick(30)


    def drawIpText(self):

        self.gameWindow.blit(self.text.render("Enter the ip address: ", True, sky), (ipTextX, ipTextY))
        self.gameWindow.blit(self.text.render(self.ipAdress, True, white), (ipTextX, ipTextY + 40))


    def drawConnectButton(self, connectX, connectY):

        if connectX and connectY:
            pygame.draw.rect(self.gameWindow, sky, (connectButtonX, connectButtonY, connectButtonWidth, connectButtonHeigth))
        else:
            pygame.draw.rect(self.gameWindow, blue, (connectButtonX, connectButtonY, connectButtonWidth, connectButtonHeigth))

        self.gameWindow.blit(self.buttonText.render("CONNECT", True, black), (connectButtonX + 10, connectButtonY + 7))

    def drawFileText(self):

        self.gameWindow.blit(self.text.render("Enter the file path: ", True, sky), (fileTextX, fileTextY))
        self.gameWindow.blit(self.text.render(self.filePath, True, white), (fileTextX, fileTextY + 40))

    def drawAnalyzeButton(self, analyzeX, analyzeY):

        if analyzeX and analyzeY:
            pygame.draw.rect(self.gameWindow, sky, (analyzeButtonX, analyzeButtonY, analyzeButtonWidth, analyzeButtonHeigth))
        else:
            pygame.draw.rect(self.gameWindow, blue, (analyzeButtonX, analyzeButtonY, analyzeButtonWidth, analyzeButtonHeigth))

        self.gameWindow.blit(self.buttonText.render("ANALYZE", True, black), (analyzeButtonX + 10, analyzeButtonY + 7))

    def drawOutputText(self):
        self.gameWindow.blit(self.text.render("Output: ", True, sky), (outputTextX, outputTextY))
        for i in range(len(self.output)):
            self.gameWindow.blit(self.text.render(self.output[i], True, white), (outputTextX, outputTextY + i*40))

    def handleNumericKeyboard(self, event):

        if self.actualText == 1:
            text = self.ipAdress
        elif self.actualText == 2:
            text = self.filePath

        if event.key == pygame.K_0:
            text += str(0)
        elif event.key == pygame.K_1:
            text += str(1)
        elif event.key == pygame.K_2:
            text+= str(2)
        elif event.key == pygame.K_3:
            text += str(3)
        elif event.key == pygame.K_4:
            text += str(4)
        elif event.key == pygame.K_5:
            text += str(5)
        elif event.key == pygame.K_6:
            text += str(6)
        elif event.key == pygame.K_7:
            text += str(7)
        elif event.key == pygame.K_8:
            text += str(8)
        elif event.key == pygame.K_9:
            text += str(9)

        if self.actualText == 1:
            self.ipAdress = text
        elif self.actualText == 2:
            self.filePath = text

    def handleLetterKeyboard(self, event):

        if self.actualText == 1:
            text = self.ipAdress
        elif self.actualText == 2:
            text = self.filePath

        if event.key == pygame.K_a:
            text += "a"
        elif event.key == pygame.K_b:
            text += "b"
        elif event.key == pygame.K_c:
            text += "c"
        elif event.key == pygame.K_d:
            text += "d"
        elif event.key == pygame.K_e:
            text += "e"
        elif event.key == pygame.K_f:
            text += "f"
        elif event.key == pygame.K_g:
            text += "g"
        elif event.key == pygame.K_h:
            text += "h"
        elif event.key == pygame.K_i:
            text += "i"
        elif event.key == pygame.K_j:
            text += "j"
        elif event.key == pygame.K_k:
            text += "k"
        elif event.key == pygame.K_l:
            text += "l"
        elif event.key == pygame.K_m:
            text += "m"
        elif event.key == pygame.K_n:
            text += "n"
        elif event.key == pygame.K_o:
            text += "o"
        elif event.key == pygame.K_p:
            text += "p"
        elif event.key == pygame.K_q:
            text += "q"
        elif event.key == pygame.K_r:
            text += "r"
        elif event.key == pygame.K_s:
            text += "s"
        elif event.key == pygame.K_t:
            text += "t"
        elif event.key == pygame.K_u:
            text += "u"
        elif event.key == pygame.K_v:
            text += "v"
        elif event.key == pygame.K_w:
            text += "w"
        elif event.key == pygame.K_x:
            text += "x"
        elif event.key == pygame.K_y:
            text += "y"
        elif event.key == pygame.K_z:
            text += "z"
        elif event.key == pygame.K_SLASH:
            text += "/"
        elif event.key == pygame.K_PERIOD:
            text += "."
        elif event.key == pygame.K_BACKSPACE:
            fileText = text[:-1]
            text = fileText
        elif event.key == pygame.K_SPACE:
            text += " "

        if self.actualText == 1:
            self.ipAdress = text
        elif self.actualText == 2:
            self.filePath = text

if __name__ == "__main__":
    gui = GUI()
    gui.startGUI()
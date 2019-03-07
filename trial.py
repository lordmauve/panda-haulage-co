from direct.showbase.ShowBase import ShowBase
from direct.task import Task


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        self.car = self.loader.loadModel("raceCarOrange.egg")
        self.car.reparentTo(self.render)

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, -1)

        self.car_y = 0

        self.taskMgr.add(self.moveCameraTask, "moveCamera")

    def run(self):
        super().run()

    def moveCameraTask(self, task):
        self.car_y += 0.01
        self.car.setPos(0, self.car_y, 0)
        self.camera.setPos(10, self.car_y - 10, 12)
        self.camera.setHpr(45, -45, 0)
        return Task.cont


if __name__ == '__main__':
    app = MyApp()
    app.run()

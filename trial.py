from direct.showbase.ShowBase import ShowBase
from direct.task import Task


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.cars = []

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, -1)

        self.car_y = 0
        self.zoom = 1.2

        self.taskMgr.add(self.moveCameraTask, "moveCamera")
        self.taskMgr.doMethodLater(2, self.next_car, "add car task")

        self.add_car()

    def add_car(self):
        car = self.loader.loadModel("truck.egg")
        car.reparentTo(self.render)
        car.setHpr(180, 0, 0)
        car.setPos(0, self.car_y - (10 * len(self.cars)), 0)
        self.cars.append(car)

    def run(self):
        super().run()

    def moveCameraTask(self, task):
        self.car_y += 0.01
        for i, car in enumerate(self.cars):
            car.setPos(0, self.car_y - (10 * i), 0)
        self.camera.setPos(10 * self.zoom, self.car_y - 10 * self.zoom, 15 * self.zoom)
        self.camera.setHpr(45, -45, 0)
        return Task.cont

    def next_car(self, task):
        self.add_car()
        self.zoom += 1.2
        task.delayTime = 2
        return task.again

if __name__ == '__main__':
    app = MyApp()
    app.run()

import preferencesDlg, compositionView
from includes import *
from viewportManager import *
from prototypeObjects import PrototypeManager
from tools import *
from panel import *
from solutionView import *
from parameters import Settings
from geosolver import randomproblem 

from ui_randomProblemDialog import Ui_randomProblemDialog

class Ui_MainWindow(QtGui.QMainWindow):
    # Ui_MainWindow: creation of the main window with al its content
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setWindowTitle(self.tr("Geometric Constraint Solver"))
        self.activatedTool = None
        self.settings = Settings()
        self.saveFileName = QtCore.QString("")
        self.createViewportManager()
        self.createDecompositionView()
        self.createSolutionView()
        self.createActions()
        self.createTriggers()
        self.createPanel()
        self.createMenus()
        self.createStatusBar()
        self.createToolbar()
                        
        self.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(self.minimumSizeHint()))    
                
    def createActions(self):
        # the actions which the user can select from the menu
        self.actionNew = QtGui.QAction(self.tr("&New"), self)
        self.actionNew.setShortcut(self.tr("Ctrl+N"))
        self.actionOpen = QtGui.QAction(self.tr("&Open"), self)
        self.actionOpen.setShortcut(self.tr("Ctrl+O"))
        self.actionSave = QtGui.QAction(self.tr("&Save"), self)
        self.actionSave.setShortcut(self.tr("Ctrl+S"))
        self.actionSave_As = QtGui.QAction(self.tr("Save &As .."), self)
        self.actionSave_As.setShortcut(self.tr("Ctrl+A"))
        self.actionImport = QtGui.QAction(self.tr("&Import"), self)
        self.actionImport.setShortcut(self.tr("Ctrl+I"))
        self.actionClose = QtGui.QAction(self.tr("&Close"), self)
        self.actionClose.setShortcut(self.tr("Ctrl+C"))
        self.actionQuit = QtGui.QAction(self.tr("E&xit"), self)
        self.actionQuit.setShortcut(self.tr("Ctrl+X"))
        # Rick 20090522
        self.actionGenerate = QtGui.QAction(self.tr("&Generate"), self)
        self.actionGenerate.setShortcut(self.tr("Ctrl+G"))

        self.editGroup = QtGui.QActionGroup(self)
        self.editGroup.setExclusive(True)
        self.actionSelect = QtGui.QAction(self.tr("Select"), self)
        self.actionSelect.setCheckable(True)    
        self.actionPlacePoint = QtGui.QAction(self.tr("Point"), self)
        self.actionPlacePoint.setCheckable(True)    
        self.actionMove = QtGui.QAction(self.tr("Move"), self)
        self.actionMove.setCheckable(True)
        self.actionConnect = QtGui.QAction(self.tr("Connect"), self)
        self.actionConnect.setCheckable(True)    
        self.actionDistanceConstraint = QtGui.QAction(self.tr("Distance"), self)
        self.actionDistanceConstraint.setCheckable(True)
        self.actionDistance = QtGui.QAction(self.tr("Line"), self)
        self.actionDistance.setCheckable(True)
        self.actionAngleConstraint = QtGui.QAction(self.tr("Angle"), self)
        self.actionAngleConstraint.setCheckable(True)
        self.actionFixedConstraint = QtGui.QAction(self.tr("Fixed"), self)
        self.actionFixedConstraint.setCheckable(True)
        
        self.actionMinMaxView = QtGui.QAction(self.tr("MM"), self)
        self.actionSolve = QtGui.QAction(self.tr("Solve"), self)
        self.actionClusters = QtGui.QAction(self.tr("Clusters"), self)
        
        self.editGroup.addAction(self.actionSelect)
        self.editGroup.addAction(self.actionPlacePoint)
        self.editGroup.addAction(self.actionMove)
        self.editGroup.addAction(self.actionConnect)
        self.editGroup.addAction(self.actionDistanceConstraint)
        self.editGroup.addAction(self.actionAngleConstraint)
        self.editGroup.addAction(self.actionDistance)
        self.editGroup.addAction(self.actionFixedConstraint)
        
        self.actionCompositionView = QtGui.QAction(self.tr("Composition View"), self)
        self.actionSolutionView = QtGui.QAction(self.tr("Solution View"), self)
        self.actionPreferences = QtGui.QAction(self.tr("Preferences"), self)        

    def createTriggers(self):
        # menu actions
        QtCore.QObject.connect(self.actionNew,QtCore.SIGNAL("triggered()"),self.new)
        QtCore.QObject.connect(self.actionQuit,QtCore.SIGNAL("triggered()"),self.close)
        QtCore.QObject.connect(self.actionSave,QtCore.SIGNAL("triggered()"),self.save)
        QtCore.QObject.connect(self.actionSave_As,QtCore.SIGNAL("triggered()"),self.saveAs)
        QtCore.QObject.connect(self.actionImport,QtCore.SIGNAL("triggered()"),self.importFile)
        QtCore.QObject.connect(self.actionOpen,QtCore.SIGNAL("triggered()"),self.load)

        QtCore.QObject.connect(self.actionCompositionView,QtCore.SIGNAL("triggered()"), self.showCompositionView)
        QtCore.QObject.connect(self.actionSolutionView,QtCore.SIGNAL("triggered()"), self.showSolutionView)
        QtCore.QObject.connect(self.actionPreferences,QtCore.SIGNAL("triggered()"), self.showPreferencesDlg)
        
        QtCore.QObject.connect(self.actionSelect,QtCore.SIGNAL("changed()"), self.selectTriggered)
        QtCore.QObject.connect(self.actionPlacePoint,QtCore.SIGNAL("changed()"), self.placePointTriggered)
        QtCore.QObject.connect(self.actionMove,QtCore.SIGNAL("changed()"), self.moveTriggered)
        QtCore.QObject.connect(self.actionConnect,QtCore.SIGNAL("changed()"), self.connectTriggered)
        QtCore.QObject.connect(self.actionDistanceConstraint,QtCore.SIGNAL("changed()"), self.distanceConstraintTriggered)    
        QtCore.QObject.connect(self.actionMinMaxView,QtCore.SIGNAL("triggered()"), self.viewportManager.minmaxView)
        

        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), PrototypeManager().solve)
        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), self.compositionView.createDecomposition)
        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), self.solutionView.createSolution)
        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), self.viewportManager.updateSolution)
        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), self.viewportManager.updateDecomposition)
        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), self.viewportManager.updateViewports)
        QtCore.QObject.connect(self.actionSolve,QtCore.SIGNAL("triggered()"), self.updateConstraintInfo)


        QtCore.QObject.connect(self.actionClusters,QtCore.SIGNAL("triggered()"), self.showClusters)
        QtCore.QObject.connect(self.actionDistance,QtCore.SIGNAL("changed()"), self.placeDistanceTriggered)
        QtCore.QObject.connect(self.actionAngleConstraint,QtCore.SIGNAL("changed()"), self.placeAngleConstraintTriggered)
        QtCore.QObject.connect(self.actionFixedConstraint,QtCore.SIGNAL("changed()"), self.placeFixedConstraintTriggered)
        # Rick 20090522
        QtCore.QObject.connect(self.actionGenerate,QtCore.SIGNAL("triggered()"),self.generateRandom)


    def createMenus(self):
        # connect the defined actions with menu items
        self.menuFile = self.menuBar().addMenu(self.tr("&File"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionGenerate)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        self.menuView = self.menuBar().addMenu(self.tr("&View"))
        self.menuView.addAction(self.actionCompositionView)
        self.menuView.addAction(self.actionSolutionView)
        
        self.menuWindow = self.menuBar().addMenu(self.tr("&Window"))
        self.menuWindow.addAction(self.dock.toggleViewAction())
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionPreferences)
        
        self.menuHelp = self.menuBar().addMenu(self.tr("&Help"))
        
    def createStatusBar(self):
        # set the statusbar
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.statusSolveInfo = QtGui.QLabel("")
        self.statusbar.addPermanentWidget(self.statusSolveInfo)
        self.setStatusBar(self.statusbar)
    
    def createToolbar(self):
        self.toolbar = QtGui.QToolBar("edit actions", self)
        self.toolbar.addAction(self.actionSelect)
        self.toolbar.addAction(self.actionPlacePoint)
        self.toolbar.addAction(self.actionMove)
        self.toolbar.addAction(self.actionConnect)
        self.toolbar.addAction(self.actionDistanceConstraint)
        self.toolbar.addAction(self.actionAngleConstraint)
        self.toolbar.addAction(self.actionDistance)
        self.toolbar.addAction(self.actionFixedConstraint)
        self.toolbar.addAction(self.actionMinMaxView)
        self.toolbar.addAction(self.actionSolve)
        self.toolbar.addAction(self.actionClusters)
        self.toolbar.insertSeparator(self.actionMinMaxView)
        self.toolbar.insertSeparator(self.actionSolve)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

    def createViewportManager(self):
        self.viewportManager = ViewportManager(self)
        self.viewportManager.showViewport(DisplayViewport.ALL, None)
        self.updateTool = UpdateToolCommand(self.viewportManager)
        
    def createPanel(self):
        self.dock = QtGui.QDockWidget(self.tr("Prototypes"), self)
        self.maxWidth = self.dock.maximumWidth()
        self.dock.setMaximumWidth(240)        
        self.dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.infoPanel = Panel(self, self.dock)
        self.dock.setWidget(self.infoPanel)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)
            
    def createDecompositionView(self):
        self.compositionView = CompositionView(None, self.viewportManager, ViewportType.DECOMPOSITION ,PrototypeManager())    
    
    def createSolutionView(self):
        self.solutionView = SolutionView(self, self.viewportManager, ViewportType.SOLUTION ,PrototypeManager())
        
        #self.viewPanelSplitter.setSizes([400, 200])
            
    def updateWindow(self):    
        self.viewportManager.updateViewports()
    
    def showCompositionView(self):
        self.compositionView.show()
    
    def showSolutionView(self):
        self.solutionView.show()
    
    def updateConstraintInfo(self):
        self.infoPanel.reset()
        updateTaskbarCommand = UpdateTextInTaskbarCommand(PrototypeManager(), self)
        updateTaskbarCommand.execute()
    
    def showClusters(self):
        prtManager = PrototypeManager()
        prtManager.showClusters()
        self.viewportManager.updateViewports()
    
    def showPreferencesDlg(self):
        self.preferencesDlg = preferencesDlg.PreferencesDlg(self.viewportManager)
        self.preferencesDlg.exec_()

    def selectTriggered(self):
        if self.actionSelect.isChecked():
            self.updateTool.execute(SelectTool())

    def placePointTriggered(self):
        if self.actionPlacePoint.isChecked():
            self.updateTool.execute(PlacePointTool())

    def distanceConstraintTriggered(self):
        if self.actionDistanceConstraint.isChecked():
            self.updateTool.execute(PlaceDistanceConstraintTool())
        
    def moveTriggered(self):
        if self.actionMove.isChecked():
            self.updateTool.execute(MoveTool())
    
    def connectTriggered(self):
        if self.actionConnect.isChecked():
            self.updateTool.execute(ConnectTool())
        
    def placeDistanceTriggered(self):
        if self.actionDistance.isChecked():
            self.updateTool.execute(PlaceDistanceTool())
    
    def placeFixedConstraintTriggered(self):
        if self.actionFixedConstraint.isChecked():
            self.updateTool.execute(PlaceFixedConstraintTool())

    def placeAngleConstraintTriggered(self):
        if self.actionAngleConstraint.isChecked():
            self.updateTool.execute(PlaceAngleConstraintTool())
    
    def new(self):
        result = QtGui.QMessageBox.warning(self, self.tr("New Scene"), self.tr("The scene may have been modified.\n" "Do you want to save your changes?"), \
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes:
            self.save()
        elif result == QtGui.QMessageBox.Cancel:
            return
            
        self.newCommand = ClearSceneCommand(self)
        self.newCommand.execute()
        self.setWindowTitle(self.tr("Geometric Constraint Solver"))
    
    def load(self):
        result = QtGui.QMessageBox.warning(self, self.tr("Scene Changes"), self.tr("The scene may have been modified.\n" "Do you want to save your changes?"), \
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes:
            self.save()
        elif result == QtGui.QMessageBox.Cancel:
            return        

        filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open File"), "", self.tr("GCS Files (*.gcs)"))
        if not filename.isEmpty():
            self.newCommand = ClearSceneCommand(self)
            self.newCommand.execute()
            self.saveFileName = filename
            self.loadCommand = LoadCommand(self)
            self.loadCommand.execute(self.saveFileName)
            nameForTitle = QtCore.QString(self.saveFileName)
            title = nameForTitle.remove(0, nameForTitle.lastIndexOf("/")+1)
            self.setWindowTitle("- " + title + self.tr(" - Geometric Constraint Solver"))

    def save(self):
        if self.saveFileName.isEmpty():
            self.saveAs()
        else:
            self.saveCommand = SaveCommand(self)
            self.saveCommand.execute(self.saveFileName)
            nameForTitle = QtCore.QString(self.saveFileName)
            title = nameForTitle.remove(0, nameForTitle.lastIndexOf("/")+1)
            self.setWindowTitle("- " + title + self.tr(" - Geometric Constraint Solver"))
    
    def saveAs(self):
        saveDialog = QtGui.QFileDialog()
        saveDialog.setDefaultSuffix(".gcs")
        filename = saveDialog.getSaveFileName(self, self.tr("Save As.."), "", self.tr("GCS Files (*.gcs)"))
        
        if not filename.isEmpty():
            if not filename.endsWith(saveDialog.defaultSuffix()):
                filename.append(saveDialog.defaultSuffix())
            self.saveFileName = filename
            self.save()

    def importFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Import File"), "", self.tr("GCS Files (*.gcs)"))
        if not filename.isEmpty():
            self.importCommand = ImportCommand(self)
            self.importCommand.execute(filename)

    # Rick 20090522
    def generateRandom(self):
        ## first do as if File->New was selected
        self.new()
        ## then show randomProblemDialog
        #ui = Ui_randomProblemDialog()
        #dialog = QtDialog()
        ## create random problem
        (numpoints, ratio, size, rounding) = (10, 0.0, 100.0, 0.0)
        problem = randomproblem.random_triangular_problem_3D(numpoints, size, rounding, ratio)
        prototypeManager = PrototypeManager()
        prototypeManager.setProblem(problem)
        self.viewportManager.updateViewports()
        ## set window title
        #title = "Untitled"
        #self.setWindowTitle(title + self.tr(" - Geometric Constraint Solver"))


    def tr(self, string):
        return QtGui.QApplication.translate("Ui_MainWindow", string, None, QtGui.QApplication.UnicodeUTF8)
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

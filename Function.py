# Импорт numpy для создания и проведения операции над матрицами,
# config для считывания глобальных переменных
# и OutputFrame для вызова окон с результатами
import numpy as np
import random
import config as cfg
from OutputFrame import ResultsTable, MatrixOutput

# Главная функция для построения маршрута
def calculate():
  
    # Преобразования двух глобальных переменных в numpy аналоги 
    # для использования встроенных функций numpy
    cfg.Length = np.array(cfg.Length)
    cfg.DistanceMatrix = np.matrix(cfg.DistanceMatrix)
   
    # Генерация коэффициентов непрямолинейности движения
    if cfg.Alpha:
        cfg.Nonlinearcoef =  np.zeros((cfg.CountOfColumbs+1,cfg.CountOfColumbs+1))
        Xshape, Yshape = cfg.Nonlinearcoef.shape
        for i in range (Xshape):
            for j in range(Yshape):
                if (i != j):
                    cfg.Nonlinearcoef[i,j] = float('{:.2f}'.format(random.uniform(1, (1+cfg.Alpha))))
        cfg.DistanceMatrix = np.multiply(cfg.DistanceMatrix, cfg.Nonlinearcoef)
        MatrixOutput(cfg.app, cfg.Nonlinearcoef, "Коэффициент непрямолинейности движения")

    # Матрица затрат времени - сколько времени требуется рабочему чтобы
    # дойти до КЯ и забрать все артикулы
    cfg.TimeConsume = np.zeros((cfg.CountOfColumbs+1,cfg.CountOfColumbs+1))
    Xshape, Yshape = cfg.TimeConsume.shape
    for i in range (Xshape):
            for j in range(Yshape):
                if (i != j):
                    cfg.TimeConsume[i,j] = (cfg.DistanceMatrix[i,j] \
                    /cfg.WorkerSpeed+ cfg.TimeToCollect*cfg.Articles[j])

    MatrixOutput(cfg.app, cfg.TimeConsume, "Матрица затрат времени")

    # Матрица экономии времени - сколько времени будет сэкономлено если 
    # объяденить два КЯ в один маршрут. Случаи когда объядинение приводит 
    # к потере времени обозначены нулями.
    cfg.TimeSaving = np.zeros((cfg.CountOfColumbs+1,cfg.CountOfColumbs+1))
    Xshape, Yshape = cfg.TimeSaving.shape
    for i in range (1, Xshape):
            for j in range(1, Yshape):
                if (i != j):
                    Value = (cfg.TimeConsume[0,j] + cfg.TimeConsume[i,0] 
                    + (cfg.TimeToUnload + cfg.Length[i]/cfg.BeltSpeed) 
                    - cfg.TimeConsume[i,j])
                    if Value >= 0:
                        cfg.TimeSaving[i,j] = Value

    MatrixOutput(cfg.app, cfg.TimeSaving, "Матрица экономии времени")



    RouteIndex = 1 # Номер первого маршрута
    # Начало цикла до момента когда все КЯ опустеют
    while True:
        # Все КЯ опустели
        if cfg.Length.max() == 0:
            break
        # Выбор начальный КЯ, находящейся дальше всех от границы цеха
        ReversedLength = cfg.Length[::-1]
        EndIndex = len(ReversedLength) - np.argmax(ReversedLength) - 1
        StartIndex = EndIndex
        # Обнуление информации о маршруте
        cfg.RouteTime = 0.0
        cfg.CurrentRoute = cfg.Names[EndIndex]
        cfg.MaxRowIndex = 0
        cfg.MaxColumnIndex = 0
        cfg.CollectedArticles = cfg.Articles[StartIndex]
        cfg.RouteFinished = 0
        cfg.RouteWeight = cfg.Weight[StartIndex]*cfg.Articles[StartIndex]
        # Цикл добавляющий новые КЯ в маршрут пока это возможно
        while True:
            # Присоединять больше нечего
            if cfg.TimeSaving.max() == 0:
                FinishRoute(StartIndex, EndIndex, RouteIndex)
                break
            # Нахождение возможных кандидатов на присоединение
            cfg.MaxRowIndex = MaxInRow(cfg.TimeSaving, EndIndex)
            if StartIndex != EndIndex:
                cfg.MaxColumnIndex = MaxInColumn(cfg.TimeSaving, StartIndex)
            # Присоединение КЯ к концу маршрута 
            if (cfg.MaxColumnIndex == 0) or \
            (cfg.TimeSaving[cfg.MaxColumnIndex,StartIndex] \
             <= cfg.TimeSaving[EndIndex,cfg.MaxRowIndex]):
                EndIndex = AddEndRoute(StartIndex, EndIndex)
                if cfg.RouteFinished:
                    FinishRoute(StartIndex, EndIndex, RouteIndex)
                    break
            # Присоединение КЯ к началу маршрута
            else:
                StartIndex = AddStartRoute(StartIndex, EndIndex)
                if cfg.RouteFinished:
                    FinishRoute(StartIndex, EndIndex, RouteIndex)
                    break
        # Увеличение индекса маршрута
        RouteIndex += 1
    # Вызов окна с результатами построения маршрутов
    RT = ResultsTable(cfg.app,cfg.Result)


# Нахождение максимального элемента в строке, если их несколько 
# возвращает индекс элемента соотвествующий наиболее отдаленному
# от границы цеха КЯ
def MaxInRow(TimeSaving, EndIndex):
    if (len(np.where(TimeSaving[EndIndex,:] == \
                    TimeSaving[EndIndex,:].max())) > 1):
        A = np.where(TimeSaving[EndIndex,:] == TimeSaving[EndIndex,:].max())
        MaxLength = 0
        for index in A:
            if cfg.Length[A]>=MaxLength:
                MaxLength = cfg.Length[A]
                MaxRowIndex = A
    else:
        MaxRowIndex = TimeSaving[EndIndex,:].argmax()
    return MaxRowIndex


# Нахождение максимального элемента в столбце, если их несколько 
# возвращает индекс элемента соотвествующий наиболее отдаленному
# от границы цеха КЯ
def MaxInColumn(TimeSaving, StartIndex):
    if (len(np.where(TimeSaving[:,StartIndex] == \
                     TimeSaving[:,StartIndex].max())) > 1):
        A = np.where(TimeSaving[:,StartIndex] == \
                     TimeSaving[:,StartIndex].max())
        MaxLength = 0
        for index in A:
            if cfg.Length[A]>=MaxLength:
                MaxLength = Length[A]
                MaxColumnIndex = A
    else:
        MaxColumnIndex = TimeSaving[:,StartIndex].argmax()
    return MaxColumnIndex


# Добавляет КЯ в конец маршрута
def AddEndRoute(StartIndex, EndIndex):
    PossibleRoute = cfg.CurrentRoute + "-" + cfg.Names[cfg.MaxRowIndex]
    PossibleRouteTime = (cfg.TimeConsume[0,StartIndex] + cfg.RouteTime 
    + cfg.TimeConsume[EndIndex,cfg.MaxRowIndex] 
    + cfg.TimeConsume[cfg.MaxRowIndex,0] + cfg.TimeToUnload 
    + cfg.Length[cfg.MaxRowIndex]/cfg.BeltSpeed)
    # Если в случае добавления КЯ происходит выход за временую границу 
    # прекращает построение маршрута
    if PossibleRouteTime > cfg.MaxTime+cfg.DeviationOfTime:
        cfg.RouteFinished = 1
        cfg.TimeSaving[:,StartIndex] = 0
        cfg.TimeSaving[EndIndex,:] = 0
    # Если после добавления КЯ маршрут соответсвует временому интервалу
    elif (PossibleRouteTime <= cfg.MaxTime+cfg.DeviationOfTime) \
        and (PossibleRouteTime >= cfg.MaxTime-cfg.DeviationOfTime):
        cfg.CurrentRoute = PossibleRoute
        cfg.RouteTime = cfg.RouteTime + cfg.TimeConsume[EndIndex,cfg.MaxRowIndex]
        cfg.CollectedArticles = (cfg.CollectedArticles 
        + cfg.Articles[cfg.MaxRowIndex])
        cfg.RouteFinished = 1
        cfg.RouteWeight = (cfg.RouteWeight 
        + cfg.Articles[cfg.MaxRowIndex]*cfg.Weight[cfg.MaxRowIndex])
        cfg.TimeSaving[:,StartIndex] = 0
        cfg.TimeSaving[EndIndex,:] = 0
        cfg.TimeSaving[cfg.MaxRowIndex,:] = 0
        cfg.TimeSaving[:,cfg.MaxRowIndex] = 0
        cfg.Length[EndIndex] = 0
        EndIndex = cfg.MaxRowIndex
    # Если после добавления КЯ маршрут имеет запас по времени
    else:
        cfg.CurrentRoute = PossibleRoute
        cfg.RouteTime = (cfg.RouteTime + cfg.TimeConsume[EndIndex,
                                                        cfg.MaxRowIndex])
        cfg.CollectedArticles = (cfg.CollectedArticles 
        + cfg.Articles[cfg.MaxRowIndex])
        cfg.RouteWeight = (cfg.RouteWeight 
        + cfg.Articles[cfg.MaxRowIndex]*cfg.Weight[cfg.MaxRowIndex])
        cfg.TimeSaving[EndIndex,:] = 0
        cfg.TimeSaving[:,cfg.MaxRowIndex] = 0
        cfg.TimeSaving[cfg.MaxRowIndex,StartIndex] = 0
        cfg.Length[EndIndex] = 0
        EndIndex = cfg.MaxRowIndex
    return EndIndex

# Добавить КЯ в начало маршрута
def AddStartRoute(StartIndex, EndIndex):
    PossibleRoute = cfg.Names[cfg.MaxColumnIndex] + "-" + cfg.CurrentRoute
    PossibleRouteTime = (cfg.TimeConsume[0,cfg.MaxColumnIndex] 
    + cfg.TimeConsume[cfg.MaxColumnIndex,StartIndex] + cfg.RouteTime 
    + cfg.TimeConsume[EndIndex,0] + cfg.TimeToUnload 
    + cfg.Length[EndIndex]/cfg.BeltSpeed)
    # Если в случае добавления КЯ происходит выход за временую границу 
    # прекращает построение маршрута
    if PossibleRouteTime > cfg.MaxTime+cfg.DeviationOfTime:
        cfg.RouteFinished = 1
        cfg.TimeSaving[:,StartIndex] = 0
        cfg.TimeSaving[EndIndex,:] = 0
    # Если после добавления КЯ маршрут соответсвует временому интервалу
    elif (PossibleRouteTime <= cfg.MaxTime+cfg.DeviationOfTime) \
        and (PossibleRouteTime >= cfg.MaxTime-cfg.DeviationOfTime):
        cfg.CurrentRoute = PossibleRoute
        cfg.RouteTime = cfg.TimeConsume[cfg.MaxColumnIndex,StartIndex] + cfg.RouteTime
        cfg.CollectedArticles = (cfg.CollectedArticles 
        + cfg.Articles[cfg.MaxColumnIndex])
        cfg.RouteWeight = (cfg.RouteWeight 
        + cfg.Articles[cfg.MaxColumnIndex]*cfg.Weight[cfg.MaxColumnIndex])
        cfg.RouteFinished = 1
        cfg.TimeSaving[:,StartIndex] = 0
        cfg.TimeSaving[EndIndex,:] = 0
        cfg.TimeSaving[cfg.MaxColumnIndex,:] = 0
        cfg.TimeSaving[:,cfg.MaxColumnIndex] = 0
        cfg.Length[StartIndex] = 0
        StartIndex = cfg.MaxColumnIndex
    # Если после добавления КЯ маршрут имеет запас по времени
    else:
        cfg.CurrentRoute = PossibleRoute
        cfg.RouteTime = (cfg.RouteTime + cfg.TimeConsume[cfg.MaxColumnIndex,
                                                        StartIndex])
        cfg.CollectedArticles = (cfg.CollectedArticles 
        + cfg.Articles[cfg.MaxColumnIndex])
        cfg.RouteWeight = (cfg.RouteWeight 
        + cfg.Articles[cfg.MaxColumnIndex]*cfg.Weight[cfg.MaxColumnIndex])
        cfg.TimeSaving[:,StartIndex] = 0
        cfg.TimeSaving[cfg.MaxColumnIndex,:] = 0
        cfg.TimeSaving[EndIndex,cfg.MaxColumnIndex] = 0
        cfg.Length[StartIndex] = 0
        StartIndex = cfg.MaxColumnIndex
    return StartIndex

def FinishRoute(StartIndex, EndIndex, RouteIndex):
    cfg.CurrentRoute = (cfg.Names[0] + "-" + cfg.CurrentRoute 
    + "-" + cfg.Names[0])
    cfg.RouteTime = (cfg.TimeConsume[0,StartIndex] + cfg.RouteTime 
    + cfg.TimeConsume[EndIndex,0] + cfg.TimeToUnload 
    + cfg.Length[EndIndex]/cfg.BeltSpeed)
    cfg.Result.append([RouteIndex, cfg.CurrentRoute, '{:.1f}'.format(cfg.RouteTime), cfg.CollectedArticles, '{:.1f}'.format(cfg.RouteWeight)])
    cfg.Length[StartIndex] = 0
    cfg.Length[EndIndex] = 0


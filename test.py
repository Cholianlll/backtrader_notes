import backtrader as bt
import pandas as pd
import backtrader.indicators as btind

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = dict(period=20) 
    #* or
    # params = (('period', 20),)
    
    # lines = ('smavalue',)
    

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # pass 
        
        # * Obtain the params
        self.movav = btind.SimpleMovingAverage(self.data, period=self.p.period)
        # self.movav which is a SimpleMovingAverage indicator It has a lines attribute which contains a sma attribute in turn
        
        # self.time2 = self.movav.lines[0] * 2
        
        # slice the data
        # self.cmpval = self.data.close(-1) > self.movav.lines[0]
        self.posi = self.data.close(-1) < self.movav.lines[0]
        # self.avepass = self.time2[-3:-1]

    def next(self):
        # * Obtain data
        '''
        self.lines[0] points to self.lines.sma
        self.line points to self.lines[0]
        self.lineX point to self.lines[X]
        self.line_X point to self.lines[X]
        '''
        # self.data It has a lines attribute which contains a close attribute in turn
        self.log('Close, %.2f' % self.datas[0].close[0])
        self.log('Movav, %.2f' % self.movav[0])
        self.log('Position: %.0f' % self.posi[0])
        # self.log('Close, %.2f' % self.datas[0].lines[0][0])
        # self.log('Time2: %.2f' % self.time2.lines[0][0])
        # self.log('CmPAV: %.2f' % self.cmpval.lines[0][0])
        # self.log('Myslice: %.2f' % self.time2.lines[0][-5:0].sum())
        
        
if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    
    cerebro.broker.setcash(100000.0)
    
    datapath = ('data/BTC_1d.csv')
    
    dataframe = pd.read_csv(datapath,
                        nrows=50,
                        # skiprows = range(1,1500),
                        parse_dates=True,
                        index_col=0)
    print(dataframe.info())
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
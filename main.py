from core.standard import AnalysisStd


class Analysis(AnalysisStd):

    def say_hello(self):
        print("Say Hello")
    
    def run_analysis(self):
        return super().run_analysis()

# A_obj = Analysis()
# A_obj.run_analysis()
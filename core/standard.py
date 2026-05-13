from abc import ABC, abstractmethod

class AnalysisStd(ABC):
    
    @abstractmethod
    def run_analysis(self):
        print("ABC run_analysis")

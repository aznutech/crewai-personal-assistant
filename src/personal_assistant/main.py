from crewai.flow import Flow, listen, start
from personal_assistant.crews.dev_crew.dev_crew import DevCrew



class DevFlow(Flow):

    @start()
    def run_dev_crew(self):
        output = DevCrew().crew().kickoff(
            inputs= {
                "iftar_query":"what is iftar time in faisalabad",
                "buffet_query":"Give top 5 buffets with prices in faisalabad",
            }
        )
        return output.raw



def kickoff():
    dev_flow = DevFlow()
    result = dev_flow.kickoff()
    print(result)

def plot():
    dev_flow = DevFlow()
    dev_flow.plot()

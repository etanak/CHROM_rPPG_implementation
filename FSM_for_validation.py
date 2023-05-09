from transitions import Machine, State

class HRValidationFSM(object):
    N_alert = 5
    N_uncertain = 3
    N_recovery  = 4
    TH_CF = 6
    Diff = 5.025

    def __init__(self):
        # self.TH_CF = TH_CF
        # self.Diff = Diff
        # self.Nalert = Nalert
        self.machine = Machine(model=self, states=['stable', 'recovery', 'alert', 'uncertain'], initial='alert')
        # self.machine.add_transition('to_stable', 'initial', 'stable')
        # self.machine.add_transition('to_alert', 'initial', 'alert')
        # self.machine.add_transition('to_alert', 'stable', 'alert')
        # self.machine.add_transition('to_recovery', 'alert', 'recovery')
        # self.machine.add_transition('to_uncertain', 'alert', 'uncertain')
        # self.machine.add_transition('to_uncertain', 'recovery', 'uncertain')
        # self.alert_start_time = Nonepresent_HR

         # Initialize count variables
        self.count_uncertain = 0
        self.count_alert = 0
        self.count_recovery = 0


    # def on_enter_stable(self):
    #     print(f"Heart rate is valid: {self.present_HR}")
    #     self.display_HR = self.present_HR

    # def on_enter_alert(self):
    #     print("Heart rate is invalid")
    #     self.display_HR = 'invalid'
    #     self.alert_start_time = time.time()

    # def on_enter_recovery(self):
    #     print("Recovering from alert state")
    #     self.display_HR = 'recovering'

    # def on_enter_uncertain(self):
    #     print("Heart rate is uncertain")
    #     self.display_HR = 'uncertain'

    # def check_alert_duration(self):
    #     if self.previous_state == 'alert':
    #         duration = time.time() - self.alert_start_time
    #         if duration >= self.Nalert:
    #             self.to_uncertain()

    def validate(self,present_HR,CF):
        self.present_state = self.state
        # self.display_HR = 'initial'
        self.HR_i_last = 0

        # this should return 'initail' state  
        # while True:
        # self.present_HR, self.CF = get_values()
        # if self.previous_state != 'alert':
        #     if abs(self.present_HR - self.previous_HR) < self.Diff and self.CF > self.TH_CF:
        #         if self.previous_state == 'alert':
        #             self.to_stable()
        #     else:
        #         self.to_alert()
        # else:
        #     if self.CF > self.TH_CF:
        #         self.to_recovery()
        #     else:
        #         self.to_uncertain()

        if self.present_state == 'stable':
            if abs(present_HR - self.previous_HR) < self.Diff and CF > self.TH_CF:
                self.to_stable()
            else:
                self.to_alert()
                self.HR_i_last = present_HR   
                self.count_alert += 1
                # update i_last
                # and HR is invalild 
        elif self.present_state == 'alert':
    
            if CF > self.TH_CF:
                self.to_recovery()
                self.count_recovery += 1
                self.count_alert =0

            elif CF <= self.TH_CF:
                self.to_alert()
                self.count_alert = 0
                self.count_uncertain += 1
            elif CF <= self.TH_CF and self.count_alert < HRValidationFSM.N_alert :
                self.count_alert += 1
            ## check alert duration !!!!
            ## update i_last 
        elif self.present_state == 'uncertain':
            if CF > self.TH_CF and self.count_uncertain < HRValidationFSM.N_uncertain:
                self.to_uncertain()
                self.count_uncertain += 1
            elif CF > self.TH_CF and self.count_uncertain == HRValidationFSM.N_uncertain:
                self.to_alert()
                self.count_uncertain = 0
                self.count_alert += 1
            elif CF <= self.TH_CF :
                self.count_uncertain = 0
        elif self.present_state == 'recovery':
            ''''''
            if abs(present_HR - self.previous_HR) < self.Diff and CF > self.TH_CF and self.count_recovery == HRValidationFSM.N_recovery:
            # and abs(self.present_HR - self.HR_i_last) < self.Diff(i-i_last)
                self.to_stable()
                self.count_recovery = 0
            # if not(abs(present_HR - self.previous_HR) < self.Diff and CF > self.TH_CF and self.count_recovery == HRValidationFSM.N_recovery):
            # # and abs(self.present_HR - self.HR_i_last) < self.Diff(i-i_last)
            #     self.count_recovery = 0
            #     self.to_recovery()

            elif CF > self.TH_CF and self.count_recovery < HRValidationFSM.N_recovery:
                self.count_recovery += 1
                self.to_recovery()
            elif CF <= self.TH_CF:
                self.count_recovery = 0
                self.count_alert += 1 
                self.to_alert()


        # self.initial_state = True
        # self.previous_state = self.present_state
        self.previous_HR = present_HR
        print(f"recover_count = {self.count_recovery}")
        return self.state,self.count_recovery



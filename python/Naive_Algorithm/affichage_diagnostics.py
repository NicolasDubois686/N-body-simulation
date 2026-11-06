import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg")

class TraceurTempsReel:
    def __init__(self, d0):
        self.d0 = d0
        self.t, self.data = [], {k: [] for k in 
            ("K", "U", "E", "dE", "P", "dL", "com", "virial")}
        
        plt.ion()
        self.fig, ((a1, a2), (a3, a4)) = plt.subplots(2, 2, figsize=(11, 7))
        self.fig.canvas.manager.set_window_title("Diagnostics N-corps")
        
        # Energies
        self.l_K, = a1.plot([], [], label="K")
        self.l_U, = a1.plot([], [], label="U")
        self.l_E, = a1.plot([], [], label="E = K+U")
        a1.set_title("Energies")
        a1.legend()
        
        # Dérive relative de l'énergie
        self.l_dE, = a2.plot([], [])
        a2.set_title("|ΔE / E₀|")
        a2.set_yscale("log")
        
        # Impulsion, moment cinétique, centre de masse
        self.l_P,   = a3.plot([], [], label="‖P‖")
        self.l_dL,  = a3.plot([], [], label="‖L - L₀‖")
        self.l_com, = a3.plot([], [], label="‖com‖")
        a3.set_title("Grandeurs conservées")
        a3.set_yscale("log")
        a3.legend()
        
        # Virial
        self.l_virial, = a4.plot([], [])
        a4.axhline(1, color="gray", ls="--", lw=0.8)
        a4.set_title("Virial = 2K/|U|")
        
        self.axes = (a1, a2, a3, a4)
        for a in self.axes:
            a.set_xlabel("t")
        self.fig.tight_layout()
        
    def ajouter(self, t, d):
        eps = 1e-18 # Pour éviter log(0)
        self.t.append(t)
        D = self.data
        D["K"].append(d["K"])
        D["U"].append(d["U"])
        D["E"].append(d["E"])
        D["dE"].append(abs(d["E"] - self.d0["E"]) / abs(self.d0["E"]) + eps)
        D["P"].append(np.linalg.norm(d["P"]) + eps)
        D["dL"].append(np.linalg.norm(d["L"] - self.d0["L"]) + eps)
        D["com"].append(np.linalg.norm(d["com"]) + eps)
        D["virial"].append(d["virial"])
        
    def rafraichir(self):
        if not plt.fignum_exists(self.fig.number):
            return # fenêtre fermée par l'utilisateur
        for ligne, cle in ((self.l_K, "K"),     (self.l_U, "U"),           (self.l_E, "E"),
                           (self.l_dE, "dE"),   (self.l_P, "P"),           (self.l_dL, "dL"),
                           (self.l_com, "com"), (self.l_virial, "virial")):
            ligne.set_data(self.t, self.data[cle])
        for a in self.axes:
            a.relim()
            a.autoscale_view()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events() # Traite les événements sans bloquer
        
    def fermer(self):
        plt.clode(self.fig)
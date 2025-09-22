import numpy as np

class HEED:
    def __init__(self, wsn, p=0.05):
        """
        HEED clustering sederhana
        :param wsn: objek WSN
        :param p: probabilitas awal menjadi cluster head
        """
        self.wsn = wsn
        self.p = p

    def select_cluster_heads(self):
        n = self.wsn.num_nodes
        energy = self.wsn.energy
        prob = self.p + (energy / max(energy)) * (1 - self.p)

        # pilih cluster head secara probabilistik
        ch = []
        for i in range(n):
            if np.random.rand() < prob[i]:
                ch.append(i)

        # jika kosong, pilih minimal 1 node random
        if len(ch) == 0:
            ch = [np.random.randint(0, n)]

        self.wsn.cluster_heads = ch

        # --- Assign tiap node ke cluster head terdekat ---
        clusters = np.zeros(n, dtype=int)
        for i in range(n):
            dists = [np.linalg.norm(self.wsn.pos[i] - self.wsn.pos[ch_id]) for ch_id in ch]
            clusters[i] = ch[np.argmin(dists)]  # pilih CH terdekat

        self.wsn.clusters = clusters
        return ch
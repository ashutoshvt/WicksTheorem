import numpy as np


def construct_transcorr_H(H_1body, H_2body, info):

    # Getting parameters!
    ngen = info[0]
    nocc = info[1]
    nvir = info[2]
    H1_gg = info[3]
    H1_gc = info[4]
    F1_gg = info[5]
    F1_gc = info[6]
    F1_cc = info[7]
    V2_gg_gg = info[8]
    V2_gg_gc = info[9]
    R2_oo_vc = info[10]
    V_F12_oo_gg = info[11]
    X_F12_oo_oo = info[12]
    B_F12_oo_oo = info[13]
    R1 = info[14]

    # slices !!
    slice_o = slice(0, nocc)
    slice_v = slice(nocc, ngen)

    # Einsum expressions!!
    #  H1_R1  
    H_1body[:, :] += 1.0 * np.einsum('pw,tw->pt', H1_gc[:, :], R1)
    #  H1_R1D  
    H_1body[:, :] += 1.0 * np.einsum('tw,qw->tq', R1, H1_gc[:, :])
    #  V2_R1  
    H_2body[:, :, :, :] += 0.5 * np.einsum('pqrw,tw->pqrt', V2_gg_gc[:, :, :, :], R1)
    H_2body[:, :, :, :] += 0.5 * np.einsum('qpsw,tw->pqts', V2_gg_gc[:, :, :, :], R1)
    #  V2_R1D  
    H_2body[:, :, :, :] += 0.5 * np.einsum('tw,srqw->tqrs', R1, V2_gg_gc[:, :, :, :])
    H_2body[:, :, :, :] += 0.5 * np.einsum('tw,rspw->tpsr', R1, V2_gg_gc[:, :, :, :])
    #  F1_R1_R1  
    #  F1_R1_R1D  
    H_1body[:, :] += 0.5 * np.einsum('uz,zw,tw->ut', R1, F1_cc, R1)
    H_1body[:, :] += -0.5 * np.einsum('uz,tz,tq->uq', R1, R1, F1_gg[:, :])
    #  F1_R1D_R1  
    H_1body[:, :] += -0.5 * np.einsum('pq,qw,uw->pu', F1_gg[:, :], R1, R1)
    H_1body[:, :] += 0.5 * np.einsum('tw,wz,uz->tu', R1, F1_cc, R1)
    #  F1_R1D_R1D  
    #  H1_R2_abxy  
    #  H1_R2D_abxy  
    #  V2_R2_abxy  
    H_2body[:, :, slice_v, slice_v] += 0.25 * np.einsum('pqyx,efxy->pqfe', V2_gg_cc, R2_abxy)
    H_2body[:, :, slice_v, slice_v] += 0.25 * np.einsum('pqxy,efxy->pqef', V2_gg_cc, R2_abxy)
    #  V2_R2D_abxy  
    H_2body[slice_v, slice_v, :, :] += 0.25 * np.einsum('efxy,rsyx->efsr', R2_abxy, V2_gg_cc)
    H_2body[slice_v, slice_v, :, :] += 0.25 * np.einsum('efxy,rsxy->efrs', R2_abxy, V2_gg_cc)
    #  F1_R2_abxy_R2_abxy  
    #  F1_R2_abxy_R2D_abxy  
    #  F1_R2D_abxy_R2_abxy  
    #  F1_R2D_abxy_R2D_abxy  
    #  H1_R2_aixy  
    #  H1_R2D_aixy  
    #  V2_R2_aixy  
    H_2body[:, :, slice_o, slice_v] += 0.25 * np.einsum('pqyx,aixy->pqia', V2_gg_cc, R2_aixy)
    H_2body[:, :, slice_v, slice_o] += 0.25 * np.einsum('pqxy,aixy->pqai', V2_gg_cc, R2_aixy)
    #  V2_R2D_aixy  
    H_2body[slice_v, :, slice_v, :] += 0.25 * np.einsum('aixy,siqy->aqas', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[slice_v, slice_v] += -0.25 * np.einsum('aixy,sisy->aa', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[:, slice_v] += 0.125 * np.einsum('aixy,aiqy->qa', R2_aixy, V2_gg_gc[slice_v, slice_o, :, :])
    H_2body[slice_v, slice_o, slice_v, :] += 0.25 * np.einsum('aixy,srsy->aiar', R2_aixy, V2_gg_gc[:, :, :, :])
    H_1body[slice_v, slice_v] += -0.25 * np.einsum('aixy,sisy->aa', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[slice_o, slice_v] += 0.125 * np.einsum('aixy,sasy->ia', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[slice_v, slice_v] += 0.25 * np.einsum('aixy,sisy->aa', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[slice_v, slice_v] += -0.125 * np.einsum('aixy,irry->aa', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_2body[slice_o, :, slice_v, :] += -0.125 * np.einsum('aixy,saqy->iqas', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[slice_o, slice_v] += 0.125 * np.einsum('aixy,sasy->ia', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[:, slice_v] += -0.0625 * np.einsum('aixy,iaqy->qa', R2_aixy, V2_gg_gc[slice_o, slice_v, :, :])
    H_2body[slice_o, :, slice_v, :] += -0.125 * np.einsum('aixy,arqy->iqar', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[slice_o, slice_v] += 0.125 * np.einsum('aixy,arry->ia', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[:, slice_v] += -0.0625 * np.einsum('aixy,aiqy->qa', R2_aixy, V2_gg_gc[slice_v, slice_o, :, :])
    H_2body[slice_v, :, slice_v, :] += -0.125 * np.einsum('aixy,irqy->aqar', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_1body[slice_v, slice_v] += 0.125 * np.einsum('aixy,irry->aa', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_1body[:, slice_v] += -0.0625 * np.einsum('aixy,iaqy->qa', R2_aixy, V2_gg_gc[slice_o, slice_v, :, :])
    H_2body[slice_v, slice_o, slice_v, :] += -0.125 * np.einsum('aixy,srry->aias', R2_aixy, V2_gg_gc[:, :, :, :])
    H_1body[slice_v, slice_v] += 0.125 * np.einsum('aixy,irry->aa', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_1body[slice_o, slice_v] += -0.0625 * np.einsum('aixy,arry->ia', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[slice_o, slice_v] += -0.125 * np.einsum('aixy,sasy->ia', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[slice_o, slice_v] += 0.0625 * np.einsum('aixy,arry->ia', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[:, slice_v] += -0.125 * np.einsum('aixy,iaqy->qa', R2_aixy, V2_gg_gc[slice_o, slice_v, :, :])
    H_1body[:, slice_v] += 0.0625 * np.einsum('aixy,aiqy->qa', R2_aixy, V2_gg_gc[slice_v, slice_o, :, :])
    H_2body[slice_v, :, slice_v, :] += 0.25 * np.einsum('aixy,ripy->apar', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[slice_v, slice_v] += -0.25 * np.einsum('aixy,riry->aa', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[:, slice_v] += 0.125 * np.einsum('aixy,aipy->pa', R2_aixy, V2_gg_gc[slice_v, slice_o, :, :])
    H_2body[slice_v, slice_o, slice_v, :] += 0.25 * np.einsum('aixy,rsry->aias', R2_aixy, V2_gg_gc[:, :, :, :])
    H_1body[slice_v, slice_v] += -0.25 * np.einsum('aixy,riry->aa', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[slice_o, slice_v] += 0.125 * np.einsum('aixy,rary->ia', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[slice_v, slice_v] += 0.25 * np.einsum('aixy,riry->aa', R2_aixy, V2_gg_gc[:, slice_o, :, :])
    H_1body[slice_v, slice_v] += -0.125 * np.einsum('aixy,issy->aa', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_2body[slice_o, :, slice_v, :] += -0.125 * np.einsum('aixy,rapy->ipar', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[slice_o, slice_v] += 0.125 * np.einsum('aixy,rary->ia', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[:, slice_v] += -0.0625 * np.einsum('aixy,iapy->pa', R2_aixy, V2_gg_gc[slice_o, slice_v, :, :])
    H_2body[slice_o, :, slice_v, :] += -0.125 * np.einsum('aixy,aspy->ipas', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[slice_o, slice_v] += 0.125 * np.einsum('aixy,assy->ia', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[:, slice_v] += -0.0625 * np.einsum('aixy,aipy->pa', R2_aixy, V2_gg_gc[slice_v, slice_o, :, :])
    H_2body[slice_v, :, slice_v, :] += -0.125 * np.einsum('aixy,ispy->apas', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_1body[slice_v, slice_v] += 0.125 * np.einsum('aixy,issy->aa', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_1body[:, slice_v] += -0.0625 * np.einsum('aixy,iapy->pa', R2_aixy, V2_gg_gc[slice_o, slice_v, :, :])
    H_2body[slice_v, slice_o, slice_v, :] += -0.125 * np.einsum('aixy,rssy->aiar', R2_aixy, V2_gg_gc[:, :, :, :])
    H_1body[slice_v, slice_v] += 0.125 * np.einsum('aixy,issy->aa', R2_aixy, V2_gg_gc[slice_o, :, :, :])
    H_1body[slice_o, slice_v] += -0.0625 * np.einsum('aixy,assy->ia', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[slice_o, slice_v] += -0.125 * np.einsum('aixy,rary->ia', R2_aixy, V2_gg_gc[:, slice_v, :, :])
    H_1body[slice_o, slice_v] += 0.0625 * np.einsum('aixy,assy->ia', R2_aixy, V2_gg_gc[slice_v, :, :, :])
    H_1body[:, slice_v] += -0.125 * np.einsum('aixy,iapy->pa', R2_aixy, V2_gg_gc[slice_o, slice_v, :, :])
    H_1body[:, slice_v] += 0.0625 * np.einsum('aixy,aipy->pa', R2_aixy, V2_gg_gc[slice_v, slice_o, :, :])
    H_2body[slice_v, slice_o, :, :] += 0.25 * np.einsum('aixy,rsyx->aisr', R2_aixy, V2_gg_cc)
    H_2body[slice_v, slice_o, :, :] += 0.25 * np.einsum('aixy,rsxy->airs', R2_aixy, V2_gg_cc)
    #  F1_R2_aixy_R2_aixy  
    #  F1_R2_aixy_R2D_aixy  
    #  F1_R2D_aixy_R2_aixy  
    #  F1_R2D_aixy_R2D_aixy  

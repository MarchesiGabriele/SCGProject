
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import altair as alt
import os.path
import getpass
import platform
from pandasql import sqldf
import openpyxl


class CalcoloScostamentiSenzaIntermedi:
    async def runCalcoloScostamenti():
        username = getpass.getuser()

        pathPart1 = "/Users/"
        pathPart2 = "/Github/SCGProject/Datasets/"
        complePath = pathPart1+username+pathPart2

        if platform.system() == "Darwin":
         if(username == "marcovinciguerra"):
                dfCambio = pd.read_csv(
                complePath+"/CorrectedDatasets/dfCambio.csv")

                dfClienti = pd.read_csv(
                complePath+"/CorrectedDatasets/dfClienti.csv")

                dfConsumi = pd.read_csv(
                complePath + "/CorrectedDatasets/dfConsumi.csv")

                dfCostoOrarioConsuntivo = pd.read_csv(
                complePath+"/CorrectedDatasets/dfConsuntivo.csv")

                dfCostoOrarioBudget = pd.read_csv(
                complePath+"CorrectedDatasets/dfCostoOrario.csv")

                dfImpiegoRisorse = pd.read_csv(
                complePath+"/CorrectedDatasets/dfImpiegoRisorse.csv")

                dftuttiClienti = pd.read_csv(
                complePath+"/CorrectedDatasets/dftuttiClienti.csv")

                dfVendite = pd.read_csv(
                complePath+"/CorrectedDatasets/dfVendite.csv")

        elif(username == "davidguzman"):
                pathPart1 = "/Users/"
                pathPart2 = "/documents/Github/SCGProject/Datasets/"
                complePath = pathPart1+username+pathPart2

                dfCambio = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfCambio.csv")

                dfClienti = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfClienti.csv")

                dfConsumi = pd.read_csv(
                        complePath + "/CorrectedDatasets/dfConsumi.csv")

                dfCostoOrarioConsuntivo = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfConsuntivo.csv")

                dfCostoOrarioBudget = pd.read_csv(
                        complePath+"CorrectedDatasets/dfCostoOrario.csv")

                dfImpiegoRisorse = pd.read_csv(
                complePath+"/CorrectedDatasets/dfImpiegoRisorse.csv")

                dftuttiClienti = pd.read_csv(
                complePath+"/CorrectedDatasets/dftuttiClienti.csv")

                dfVendite = pd.read_csv(
                complePath+"/CorrectedDatasets/dfVendite.csv")

        elif platform.system() == "Linux":
                complePath = "/home/alinux/unibg/git_repo/SCGProject"
                pathPart1 = "/Users/"
                pathPart2 = "/documents/Github/SCGProject/Datasets/"
                complePath = pathPart1+username+pathPart2
                complePath = '/home/alinux/unibg/git_repo/SCGProject/Datasets/'

                dfCambio = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfCambio.csv")

                dfClienti = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfClienti.csv")

                dfConsumi = pd.read_csv(
                        complePath + "/CorrectedDatasets/dfConsumi.csv")

                dfCostoOrarioConsuntivo = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfConsuntivo.csv")

                dfCostoOrarioBudget = pd.read_csv(
                        complePath+"CorrectedDatasets/dfCostoOrario.csv")

                dfImpiegoRisorse = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfImpiegoRisorse.csv")

                dftuttiClienti = pd.read_csv(
                        complePath+"/CorrectedDatasets/dftuttiClienti.csv")

                dfVendite = pd.read_csv(
                        complePath+"/CorrectedDatasets/dfVendite.csv")



        dfCambio["TassoCambioMedio"] = dfCambio["TassoCambioMedio"].str.replace(',','.')


        # # Ricavi


        dfVendite.rename(columns = {'budget/cons':'budget'}, inplace = True)
        venditeConsuntivo = sqldf("SELECT DISTINCT * FROM dfVendite WHERE budget = 'CONSUNTIVO' or budget = 'Consuntivo'")
        venditeBudget = sqldf("SELECT DISTINCT * FROM dfVendite WHERE budget = 'BUDGET' or budget = 'Budget'")






        # join with dfCambio and dfClienti
        venditeConsuntivo = sqldf('''SELECT DISTINCT v.NrMovimento, v.budget, v.NrArticolo, v.Quantity, v.ImportoVenditaValutaLocaleTOTALEVENDITA,k.TassoCambioMedio,v.ImportoVenditaValutaLocaleTOTALEVENDITA/k.TassoCambioMedio as TotaleEuro, v.NrOrigine, c.CodCondizioniPagam, c.FattCumulative, c.Valuta
        FROM venditeConsuntivo as v join dfClienti as c on v.NrOrigine = c.Nr join dfCambio as k on c.Valuta = k.CodiceValuta
        where k.Anno = 'Consuntivo' or k.Anno = 'CONSUNTIVO'
        ''')

        venditeBudget = sqldf('''SELECT DISTINCT v.NrMovimento, v.budget, v.NrArticolo, v.Quantity, v.ImportoVenditaValutaLocaleTOTALEVENDITA,k.TassoCambioMedio,v.ImportoVenditaValutaLocaleTOTALEVENDITA/k.TassoCambioMedio as TotaleEuro, v.NrOrigine, c.CodCondizioniPagam, c.FattCumulative, c.Valuta
        FROM venditeBudget as v join dfClienti as c on v.NrOrigine = c.Nr join dfCambio as k on c.Valuta = k.CodiceValuta
        where k.Anno = 'Budget' or k.Anno = 'BUDGET'
        ''')






        sumVenditeConsuntivo = sqldf('select sum(TotaleEuro) as sumVenditaTotale from venditeConsuntivo')
        sumVenditeBudget = sqldf('select sum(TotaleEuro) as sumVenditaTotale from venditeBudget')


        # # Costi

        # Materie prime


        dfConsumi.rename(columns = {'Budget/cons':'budget'}, inplace = True)
        consumiConsuntivo = sqldf("SELECT DISTINCT * FROM dfConsumi WHERE budget = 'CONSUNTIVO'")
        consumiBudget = sqldf("SELECT DISTINCT * FROM dfConsumi WHERE budget = 'BUDGET'")
        sumConsumiConsuntivo = sqldf('select sum(ImportoCostoTOTALE) from consumiConsuntivo')
        sumConsumiBudget = sqldf('select sum(ImportoCostoTOTALE) from consumiBudget')


        # Lavorazioni interne


        impiegoConsuntivo = sqldf("SELECT DISTINCT * FROM dfImpiegoRisorse WHERE budgetConsuntivo = 'CONSUNTIVO' or budgetConsuntivo = 'Consuntivo'")
        #join con i costi orari
        impiegoConsuntivo  = sqldf('''SELECT DISTINCT i.NrArticolo,i.budgetConsuntivo,i.NrOrdineProduzione,i.Descrizione,i.NrAreaProduzione,i.Risorsa,i.QuantitydiOutput,i.TempoRisorsa,c.CostoOrario
        FROM impiegoConsuntivo as i join dfCostoOrarioConsuntivo as c 
        on c.AreaProduzione = i.NrAreaProduzione and c.Risorsa = i.Risorsa''')
        # ci sono alcune quantità di output nulle, per gestire le sommiamo alle tuple con tutte le altre cose uguali
        impiegoConsuntivoOld = sqldf('''select NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,sum(TempoRisorsa) as TempoRisorsa,CostoOrario, sum(QuantitydiOutput) as QuantitydiOutput
        from impiegoConsuntivo
        group by NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,CostoOrario
        order by NrArticolo
        ''')
        impiegoConsuntivo1 = impiegoConsuntivoOld.copy()
        # ASSUNZIONE: la quantity di output maggiore tiene conto di tutte quelle inferiori.



        impiegoConsuntivoNew = sqldf('''select NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,sum(TempoRisorsa) as TempoRisorsa,CostoOrario, max(QuantitydiOutput) as QuantitydiOutput
        from impiegoConsuntivo
        group by NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,CostoOrario
        order by NrArticolo
        ''')
        impiegoConsuntivoNew






        sqldf('select NrArticolo, NrOrdineProduzione, count(*) as c from impiegoConsuntivoNew group by NrArticolo, NrOrdineProduzione order by c')



        impiegoBudget = sqldf("SELECT DISTINCT * FROM dfImpiegoRisorse WHERE budgetConsuntivo = 'BUDGET' or budgetConsuntivo = 'Budget'")
        #join con i costi orari
        impiegoBudget = sqldf('''SELECT DISTINCT i.NrArticolo,i.budgetConsuntivo,i.NrOrdineProduzione,i.Descrizione,i.NrAreaProduzione,i.Risorsa,i.QuantitydiOutput,i.TempoRisorsa,c.CostoOrario
        FROM impiegoBudget as i join dfCostoOrarioBudget as c 
        on c.AreaProduzione = i.NrAreaProduzione and c.Risorsa = i.Risorsa''')
        # righe a consuntivo sono di più che a budget e la somma dei 2 non corrisponde al numero di righe della tabella impiego risorse

        # ci sono alcune quantità di output nulle, per gestire le sommiamo alle tuple con tutte le altre cose uguali
        impiegoBudgetOld = sqldf('''select NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,sum(TempoRisorsa) as TempoRisorsa,CostoOrario, sum(QuantitydiOutput) as QuantitydiOutput
        from impiegoBudget
        group by NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,CostoOrario
        order by NrArticolo
        ''')
        impiegoBudget1 = impiegoBudgetOld.copy()

        impiegoBudgetNew = sqldf('''select NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,sum(TempoRisorsa) as TempoRisorsa,CostoOrario, max(QuantitydiOutput) as QuantitydiOutput
        from impiegoBudget
        group by NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,CostoOrario
        order by NrArticolo
        ''')






        impiegoBudgetNew = sqldf('''select NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,sum(TempoRisorsa) as TempoRisorsa,CostoOrario, sum(QuantitydiOutput) as QuantitydiOutput
        from impiegoBudgetNew
        group by NrArticolo,budgetConsuntivo,NrOrdineProduzione,Descrizione,NrAreaProduzione,Risorsa,CostoOrario
        order by NrArticolo
        ''')



        impiegoBudgetNew

        sqldf('''select NrArticolo, NrOrdineProduzione, Descrizione, NrAreaProduzione, Risorsa, count(*)
        from impiegoBudgetNew 
        group by NrArticolo, NrOrdineProduzione, Descrizione, NrAreaProduzione, Risorsa
        order by count(*) desc''')

        sqldf('''select NrArticolo, Descrizione, NrAreaProduzione, Risorsa, count(*)
        from impiegoBudgetNew 
        group by NrArticolo, Descrizione, NrAreaProduzione, Risorsa
        order by count(*) desc''')


        # # Scostamento totale


        sumImpiegoConsuntivo = sqldf(
        'SELECT sum(TempoRisorsa*CostoOrario) FROM impiegoConsuntivoNew WHERE TempoRisorsa>=0')
        sumImpiegoBudget = sqldf(
        'SELECT sum(TempoRisorsa*CostoOrario) FROM impiegoBudgetNew WHERE TempoRisorsa>=0')





        # Senza vincoli su tempi negativi
        # 
        # **non cambia perché per ogni tempo negativo esiste un tempo positivo uguale in modulo che, al sommare i tempi delle stesse attività, si annullano a vicenda**


        sumImpiegoConsuntivo = sqldf(
        'SELECT sum(TempoRisorsa*CostoOrario) FROM impiegoConsuntivoNew')
        sumImpiegoBudget = sqldf(
        'SELECT sum(TempoRisorsa*CostoOrario) FROM impiegoBudgetNew')





        # # Socostamento di volume, impiego e prezzo per le Lavorazioni

        # #### consuntivo


        # Creazione colonna ImpiegoUnitario
        impiegoConsuntivoNew = sqldf(''' select NrArticolo, budgetConsuntivo, NrOrdineProduzione, Descrizione, NrAreaProduzione, Risorsa, TempoRisorsa, TempoRisorsa/QuantitydiOutput as ImpiegoUnitario, CostoOrario ,QuantitydiOutput
        from impiegoConsuntivoNew''')
        impiegoConsuntivoNew


        # Avg out the null values


        impiegoConsuntivoNew = sqldf(''' select NrArticolo, budgetConsuntivo, Descrizione, NrAreaProduzione, sum(TempoRisorsa) as TempoRisorsa, avg(CostoOrario) as CostoOrario, max(QuantitydiOutput) as QuantitydiOutput
        from impiegoConsuntivoNew
        group by NrArticolo, budgetConsuntivo, Descrizione, NrAreaProduzione
        ''')
        impiegoConsuntivo = sqldf(''' select NrArticolo, budgetConsuntivo, Descrizione, NrAreaProduzione, TempoRisorsa, (TempoRisorsa/QuantitydiOutput) as ImpiegoUnitario, CostoOrario,QuantitydiOutput
        from impiegoConsuntivoNew
        order by NrArticolo
        ''')



        sqldf('select sum(TempoRisorsa*CostoOrario) from impiegoConsuntivo') # si mantiene quasi uguale!!



        sqldf('select sum(ImpiegoUnitario*CostoOrario*QuantitydiOutput) from impiegoConsuntivo') 


        # la piccola differenza è dovuta alla restante parte di righe con output nulle e senza altre righe con output non nullo da sommare


        sqldf('select * from impiegoConsuntivo where ImpiegoUnitario is null') 


        # #### ripetiamo per budget


        impiegoBudgetNew = sqldf(''' select NrArticolo, budgetConsuntivo, Descrizione, NrAreaProduzione, sum(TempoRisorsa) as TempoRisorsa, avg(CostoOrario) as CostoOrario, max(QuantitydiOutput) as QuantitydiOutput
        from impiegoBudgetNew
        group by NrArticolo, budgetConsuntivo, Descrizione, NrAreaProduzione
        ''')
        impiegoBudget = sqldf(''' select NrArticolo, budgetConsuntivo, Descrizione, NrAreaProduzione, TempoRisorsa, (TempoRisorsa/QuantitydiOutput) as ImpiegoUnitario, CostoOrario,QuantitydiOutput
        from impiegoBudgetNew
        order by NrArticolo
        ''')



        sqldf('select sum(TempoRisorsa*CostoOrario) from impiegoBudget') # si mantiene quasi uguale!!



        sqldf('select sum(ImpiegoUnitario*CostoOrario*QuantitydiOutput) from impiegoBudget') 



        sqldf('select * from impiegoBudget where ImpiegoUnitario is null') 


        # #### Merge/Join


        impiegoConsuntivo.drop(['budgetConsuntivo'], axis=1, inplace=True)
        impiegoBudget.drop(['budgetConsuntivo'], axis=1, inplace=True)
        x = pd.merge(impiegoConsuntivo, impiegoBudget, on=['NrArticolo', 'Descrizione', 'NrAreaProduzione'], how='outer')
        x



        c = sqldf('select sum(ImpiegoUnitario_x*CostoOrario_x*QuantitydiOutput_x) from x').iloc[0][0]
        b = sqldf('select sum(ImpiegoUnitario_y*CostoOrario_y*QuantitydiOutput_y) from x').iloc[0][0]
        # non altera i totali!!



        #Budget Standard
        BudgetStandardLav = sqldf('select sum(ImpiegoUnitario_y*CostoOrario_y*QuantitydiOutput_y) from x').iloc[0][0]
        # Impiego Standard (volume a consuntivo)
        ImpiegoStandardLav = sqldf('select sum(ImpiegoUnitario_y*CostoOrario_y*QuantitydiOutput_x) from x').iloc[0][0]
        # Impiego Effettivo (volume e impiego a consuntivo)
        ImpiegoEffettivoLav=sqldf('select sum(ImpiegoUnitario_x*CostoOrario_y*QuantitydiOutput_x) from x').iloc[0][0]
        # Budget Effettivo (tutto a consuntivo)
        BudgetEffettivoLav=sqldf('select sum(ImpiegoUnitario_x*CostoOrario_x*QuantitydiOutput_x) from x').iloc[0][0]



        sqldf('select ImpiegoUnitario_y,CostoOrario_y,QuantitydiOutput_x from x order by QuantitydiOutput_x desc')



        #Scostamenti
        ScostamentoVolumeLav = ImpiegoStandardLav-b
        ScostamentoImpiegoLav = ImpiegoEffettivoLav-ImpiegoStandardLav
        ScostamentoPrezzoLav = BudgetEffettivoLav-ImpiegoEffettivoLav


        # # Socostamento di volume, impiego e prezzo per le materie prime

        # #### Group by CodiceMP

        # se non facciamo qualche group by a priori si sdoppiano le righe, proviamo prima con CodiceMP


        consumiConsuntivoUnitByMP = sqldf('''select CodiceMP, NrArticolo, NrDocumento as NrOrdineProduzione, sum(QuantityMPImpiegata) as QuantityMPImpiegata, sum(ImportoCostoTOTALE) as ImportoCostoTOTALE
        from consumiConsuntivo     
        group by CodiceMP, NrArticolo, NrOrdineProduzione''')
        consumiBudgetUnitByMP = sqldf('''select CodiceMP, NrArticolo,NrDocumento as NrOrdineProduzione, sum(QuantityMPImpiegata) as QuantityMPImpiegata, sum(ImportoCostoTOTALE) as ImportoCostoTOTALE
        from consumiBudget     
        group by CodiceMP, NrArticolo,NrOrdineProduzione''')
        consumiConsuntivoUnitByMP


        # ##### ritrovare volumi di produzione


        temp = sqldf('''select a.CodiceMP,a.NrArticolo,a.NrOrdineProduzione,a.QuantityMPImpiegata,a.ImportoCostoTOTALE,
        (select max(QuantitydiOutput) from impiegoConsuntivoNew  where a.NrArticolo = NrArticolo and a.NrOrdineProduzione = NrOrdineProduzione) as QuantitydiOutput
        from consumiConsuntivoUnitByMP as a''')
        temp = sqldf('''select distinct CodiceMP,NrArticolo,sum(QuantityMPImpiegata) as QuantityMPImpiegata,sum(ImportoCostoTOTALE) as ImportoCostoTOTALE ,QuantitydiOutput 
        from temp group by CodiceMP,NrArticolo''')
        temp



        temp = sqldf('''select a.CodiceMP,a.NrArticolo,a.NrOrdineProduzione,a.QuantityMPImpiegata,a.ImportoCostoTOTALE,
        (select max(QuantitydiOutput) from impiegoConsuntivoNew  where a.NrArticolo = NrArticolo and a.NrOrdineProduzione = NrOrdineProduzione) as QuantitydiOutput
        from consumiConsuntivoUnitByMP as a''')
        temp = sqldf('''select distinct CodiceMP,NrArticolo,sum(QuantityMPImpiegata) as QuantityMPImpiegata,sum(ImportoCostoTOTALE) as ImportoCostoTOTALE ,QuantitydiOutput 
        from temp group by CodiceMP,NrArticolo''')
        consumiConsuntivoVolProd = sqldf('''select distinct CodiceMP,NrArticolo,QuantityMPImpiegata/QuantitydiOutput as ImpiegoPerPezzo,ImportoCostoTOTALE/QuantityMPImpiegata as CostoPerUnitaMis,QuantitydiOutput, ImportoCostoTOTALE
        from temp group by CodiceMP,NrArticolo''')

        temp = sqldf('''select a.CodiceMP,a.NrArticolo,a.NrOrdineProduzione,a.QuantityMPImpiegata,a.ImportoCostoTOTALE,
        (select max(QuantitydiOutput) from impiegoBudgetNew  where a.NrArticolo = NrArticolo and a.NrOrdineProduzione = NrOrdineProduzione) as QuantitydiOutput
        from consumiBudgetUnitByMP as a''')
        temp = sqldf('''select distinct CodiceMP,NrArticolo,sum(QuantityMPImpiegata) as QuantityMPImpiegata,sum(ImportoCostoTOTALE) as ImportoCostoTOTALE ,QuantitydiOutput 
        from temp group by CodiceMP,NrArticolo''')
        consumiBudgetVolProd  = sqldf('''select distinct CodiceMP,NrArticolo,QuantityMPImpiegata/QuantitydiOutput as ImpiegoPerPezzo,ImportoCostoTOTALE/QuantityMPImpiegata as CostoPerUnitaMis,QuantitydiOutput, ImportoCostoTOTALE
        from temp group by CodiceMP,NrArticolo''')

        consumiConsuntivoVolProd






        # TODO rimuovere la maggior parte di quanitity nulle possibile dalle lavorazioni continua a essere importante!



        # non si perdono dei decimali 


        # ##### Scostamenti


        #consumiConsuntivoVolProd.drop(columns='NrOrdineProduzione',inplace=True)
        #consumiBudgetVolProd.drop(columns='NrOrdineProduzione',inplace=True)



        ConsumiUnit = pd.merge(consumiConsuntivoVolProd,consumiBudgetVolProd, on = ['CodiceMP','NrArticolo'], how = 'outer')
        ConsumiUnit



        BudgetEffettivoMP = sqldf('select sum(QuantitydiOutput_x*ImpiegoPerPezzo_x*CostoPerUnitaMis_x) from ConsumiUnit').iloc[0][0]
        ImpiegoEffettivoMP = sqldf('select sum(QuantitydiOutput_x*ImpiegoPerPezzo_x*CostoPerUnitaMis_y) from ConsumiUnit').iloc[0][0]
        ImpiegoStandardMP = sqldf('select sum(QuantitydiOutput_x*ImpiegoPerPezzo_y*CostoPerUnitaMis_y) from ConsumiUnit').iloc[0][0]
        BudgetStandardMP = sqldf('select sum(QuantitydiOutput_y*ImpiegoPerPezzo_y*CostoPerUnitaMis_y) from ConsumiUnit').iloc[0][0]




        ScostamentoVolumeMP =  ImpiegoStandardMP - BudgetStandardMP
        ScostamentoImpiegoMP = ImpiegoEffettivoMP-ImpiegoStandardMP
        ScostamentoPrezzoMP = BudgetEffettivoMP-ImpiegoEffettivoMP 





        # # Socostamento di volume, mix e prezzo per i ricavi

        #  group by NrArticolo dei ricavi


        venditeConsuntivoArt = sqldf('''select NrArticolo, sum(Quantity) as Quantity, sum(TotaleEuro) as TotaleEuro
                from venditeConsuntivo
                group by NrArticolo''')
        venditeConsuntivoArt



        venditeBudgetArt = sqldf('''select NrArticolo, sum(Quantity) as Quantity, sum(TotaleEuro) as TotaleEuro
                from venditeBudget
                group by NrArticolo''')
        venditeBudgetArt


        # ##### calcolo del delta dei volumi 



        vendite = pd.merge(venditeConsuntivoArt,venditeBudgetArt, on = ['NrArticolo'], how = 'outer')
        vendite



        sqldf('''select sum(TotaleEuro_x) from vendite''')



        sqldf('''select sum(TotaleEuro_y) from vendite''')



        sqldf('''select NrArticolo, Quantity_x-Quantity_y as DiffQuantity
                from vendite
                order by DiffQuantity desc
                ''')



        sqldf('''select sum(Quantity_x-Quantity_y) as DiffQuantity
                from vendite
                ''')


        # ##### creazione colonne mix, volume, prezzo unitario


        venditeBudgetS = sqldf('''select NrArticolo, (Quantity*100000000000/7224) as Mix, 7224 as VolumeTotale, TotaleEuro/Quantity as PrezzoUnitario
                from venditeBudgetArt''')
        venditeBudgetS



        sqldf('select sum(Mix*VolumeTotale*PrezzoUnitario)/100000000000 from venditeBudgetS')



        sqldf('select sum(Quantity) from venditeConsuntivo')



        venditeConsuntivoS = sqldf('''select NrArticolo, (Quantity*100000000000/9329) as Mix, 9329 as VolumeTotale, TotaleEuro/Quantity as PrezzoUnitario
                from venditeConsuntivoArt''')
        venditeConsuntivoS



        sqldf('select sum(Mix*VolumeTotale*PrezzoUnitario)/100000000000 from venditeConsuntivoS')


        # ### Calcolo socostamenti di volume, mix e prezzo


        venditeS = pd.merge(venditeConsuntivoS, venditeBudgetS, on = ['NrArticolo'], how = 'outer')
        venditeS



        sqldf('select sum(Mix_x*VolumeTotale_x*PrezzoUnitario_x)/100000000000 from venditeS')



        z = sqldf('select NrArticolo,(Mix_y*VolumeTotale_y*PrezzoUnitario_y)/100000000000 as c from venditeS ')
        z



        BudgetStandardRic = sqldf('select sum(Mix_y*VolumeTotale_y*PrezzoUnitario_y)/100000000000 from venditeS ').iloc[0][0]
        MixStandardRic = sqldf('select sum(Mix_y*VolumeTotale_x*PrezzoUnitario_y)/100000000000 from venditeS ').iloc[0][0]
        MixEffettivoRic = sqldf('select sum(Mix_x*VolumeTotale_x*PrezzoUnitario_y)/100000000000 from venditeS ').iloc[0][0]
        BudgetEffettivoRic = sqldf('select sum(Mix_x*VolumeTotale_x*PrezzoUnitario_x)/100000000000 from venditeS ').iloc[0][0]






        ScostamentoVolumeRic = MixStandardRic-BudgetStandardRic
        ScostamentoMixRic = MixEffettivoRic-MixStandardRic
        ScostamentoPrezzoRic = BudgetEffettivoRic-MixEffettivoRic





        # # Vista globale degli scostamenti


        data = {'Index': ['Ricavi', 'CostiMP', 'CostiLav', 'Margine'], 
                'Budget' : [BudgetStandardRic, BudgetStandardMP,BudgetStandardLav, (BudgetStandardRic - (BudgetStandardMP+BudgetStandardLav))],
                'ScostamentoVolume' : [ScostamentoVolumeRic,ScostamentoVolumeMP,ScostamentoVolumeLav, (ScostamentoVolumeRic - (ScostamentoVolumeMP+ScostamentoVolumeLav))], 
                'MixStandard' : [MixStandardRic, ImpiegoStandardMP,ImpiegoStandardLav, (MixStandardRic - (ImpiegoStandardMP+ImpiegoStandardLav))],
                'ScostamentoMix' : [ScostamentoMixRic,ScostamentoImpiegoMP,ScostamentoImpiegoLav, (ScostamentoMixRic - (ScostamentoImpiegoMP+ScostamentoImpiegoLav))],
                'MixEffettivo' : [MixEffettivoRic, ImpiegoEffettivoMP,ImpiegoEffettivoLav, (MixEffettivoRic - (ImpiegoEffettivoMP+ImpiegoEffettivoLav))],
                'ScostamentoPrezzo' : [ScostamentoPrezzoRic,ScostamentoPrezzoMP,ScostamentoPrezzoLav, (ScostamentoPrezzoRic - (ScostamentoPrezzoMP+ScostamentoPrezzoLav))], 
                'Consuntivo' : [BudgetEffettivoRic, BudgetEffettivoMP, BudgetEffettivoLav, (BudgetEffettivoRic - (BudgetEffettivoMP+BudgetEffettivoLav))],
                'ScostamentoTotale' : [BudgetEffettivoRic-BudgetStandardRic,BudgetEffettivoMP-BudgetStandardMP,BudgetEffettivoLav-BudgetStandardLav, (BudgetEffettivoRic - BudgetStandardRic - (BudgetEffettivoMP-BudgetStandardMP+BudgetEffettivoLav-BudgetStandardLav))]}



        pd.DataFrame(data)





        # # Repeat ma tenendo conto della valuta


        venditeConsuntivoArt = sqldf('''select NrArticolo, sum(Quantity) as Quantity,  sum(ImportoVenditaValutaLocaleTOTALEVENDITA) as TotaleLocale, Valuta, TassoCambioMedio
                from venditeConsuntivo
                group by NrArticolo, Valuta, TassoCambioMedio''')
        venditeBudgetArt = sqldf('''select NrArticolo, sum(Quantity) as Quantity, sum(ImportoVenditaValutaLocaleTOTALEVENDITA) as TotaleLocale, Valuta, TassoCambioMedio
                from venditeBudget
                group by NrArticolo, Valuta, TassoCambioMedio ''')



        venditeBudgetArt


        # ##### creazione colonne mix, volume, prezzo unitario (locale)


        venditeConsuntivoS = sqldf('''select NrArticolo, (Quantity*100000000000/9329) as Mix, 9329 as VolumeTotale, TotaleLocale/Quantity as PrezzoUnitario, Valuta, TassoCambioMedio, (TotaleLocale/Quantity)/TassoCambioMedio as PrezzoUnitarioEuro
                from venditeConsuntivoArt''')
        venditeBudgetS = sqldf('''select NrArticolo, (Quantity*100000000000/7224) as Mix, 7224 as VolumeTotale, TotaleLocale/Quantity as PrezzoUnitario, Valuta, TassoCambioMedio, (TotaleLocale/Quantity)/TassoCambioMedio as PrezzoUnitarioEuro
                from venditeBudgetArt''')


        # ### Calcolo socostamenti di volume, mix, prezzo e valuta


        venditeS1 = pd.merge(venditeConsuntivoS, venditeBudgetS, on = ['NrArticolo', 'Valuta'], how = 'outer')
        venditeS1
        #venditeS1.to_excel('venditeS1.xlsx')



        BudgetStandardRic = sqldf('select sum(Mix_y*VolumeTotale_y*PrezzoUnitario_y/TassoCambioMedio_y)/100000000000 from venditeS1 ').iloc[0][0]
        MixStandardRic = sqldf('select sum(Mix_y*VolumeTotale_x*PrezzoUnitario_y/TassoCambioMedio_y)/100000000000 from venditeS1 ').iloc[0][0]
        MixEffettivoRic = sqldf('select sum(Mix_x*VolumeTotale_x*PrezzoUnitario_y/TassoCambioMedio_y)/100000000000 from venditeS1 ').iloc[0][0]
        BudgetEffettivoRic = sqldf('select sum(Mix_x*VolumeTotale_x*PrezzoUnitario_x/TassoCambioMedio_y)/100000000000 from venditeS1 ').iloc[0][0]
        BudgetEffettivoValutaRic = sqldf('select sum(Mix_x*VolumeTotale_x*PrezzoUnitario_x/TassoCambioMedio_x)/100000000000 from venditeS1 ').iloc[0][0]






        ScostamentoVolumeRic = MixStandardRic-BudgetStandardRic
        ScostamentoMixRic = MixEffettivoRic-MixStandardRic
        ScostamentoPrezzoRic = BudgetEffettivoRic-MixEffettivoRic
        ScostamentoValutaRic = BudgetEffettivoValutaRic-BudgetEffettivoRic





        # # Vista globale degli scostamenti v2


        data = {'Index': ['Ricavi', 'CostiMP', 'CostiLav', 'Margine'], 
                'Budget' : [BudgetStandardRic, BudgetStandardMP,BudgetStandardLav, (BudgetStandardRic - (BudgetStandardMP+BudgetStandardLav))],
                'ScostamentoVolume' : [ScostamentoVolumeRic,ScostamentoVolumeMP,ScostamentoVolumeLav, (ScostamentoVolumeRic - (ScostamentoVolumeMP+ScostamentoVolumeLav))], 
                'MixStandard' : [MixStandardRic, ImpiegoStandardMP,ImpiegoStandardLav, (MixStandardRic - (ImpiegoStandardMP+ImpiegoStandardLav))],
                'ScostamentoMix' : [ScostamentoMixRic,ScostamentoImpiegoMP,ScostamentoImpiegoLav, (ScostamentoMixRic - (ScostamentoImpiegoMP+ScostamentoImpiegoLav))],
                'MixEffettivo' : [MixEffettivoRic, ImpiegoEffettivoMP,ImpiegoEffettivoLav, (MixEffettivoRic - (ImpiegoEffettivoMP+ImpiegoEffettivoLav))],
                'ScostamentoPrezzo' : [ScostamentoPrezzoRic,ScostamentoPrezzoMP,ScostamentoPrezzoLav, (ScostamentoPrezzoRic - (ScostamentoPrezzoMP+ScostamentoPrezzoLav))], 
                'MixValuta' : [BudgetEffettivoRic, BudgetEffettivoMP,BudgetEffettivoLav, (BudgetEffettivoRic - (BudgetEffettivoMP+BudgetEffettivoLav))],
                'ScostamentoValuta' : [ScostamentoValutaRic, 0, 0, (ScostamentoValutaRic - (0+0))],
                'Consuntivo' : [BudgetEffettivoValutaRic, BudgetEffettivoMP, BudgetEffettivoLav, (BudgetEffettivoValutaRic - (BudgetEffettivoMP+BudgetEffettivoLav))],
                'ScostamentoTotale' : [BudgetEffettivoValutaRic-BudgetStandardRic,BudgetEffettivoMP-BudgetStandardMP,BudgetEffettivoLav-BudgetStandardLav, (BudgetEffettivoValutaRic - BudgetStandardRic - (BudgetEffettivoMP-BudgetStandardMP+BudgetEffettivoLav-BudgetStandardLav))]}



        pd.DataFrame(data)



        60668.847371-111679.240361-38006.143020-61546.894857


        # come vedremo, i volumi di vendita non coincidono ai volumi di produzione, come negli esercizi fatti a lezione.
        # 
        # Invece, a budget, si vendenono circa 412 prodotti diversi, mentre si lavorano circa 503, dei quali soltanto 73 passano per una fase di montaggio nell'anno in quesitone.
        # 
        # Questo ci porta alla conclusione che ci sono delle rimanenze, e non tutto cio che e prodotto nell'anno e venduto nello stesso anno.


        impiegoBudgetNew



        sqldf('select NrArticolo, QuantitydiOutput from impiegoBudgetNew group by NrArticolo,QuantitydiOutput order by NrArticolo')



        sqldf('select NrArticolo,Quantity from venditeBudget group by NrArticolo,Quantity order by NrArticolo')



        sqldf('select NrArticolo,sum(Quantity) as quantita from venditeBudget group by NrArticolo order by NrArticolo')



        sqldf("SELECT DISTINCT NrArticolo FROM dfImpiegoRisorse WHERE (budgetConsuntivo = 'BUDGET' or budgetConsuntivo = 'Budget')")



        sqldf("SELECT DISTINCT NrArticolo,QuantitydiOutput FROM dfImpiegoRisorse WHERE (budgetConsuntivo = 'BUDGET' or budgetConsuntivo = 'Budget') and Descrizione = 'Montaggio'")



        pd.merge(
        sqldf('select NrArticolo,sum(Quantity) as quantita from venditeBudget group by NrArticolo order by NrArticolo'),
        sqldf("SELECT DISTINCT NrArticolo,QuantitydiOutput FROM dfImpiegoRisorse WHERE (budgetConsuntivo = 'BUDGET' or budgetConsuntivo = 'Budget') and Descrizione = 'Montaggio'"), 
        on='NrArticolo', how='outer')



        venditeConsuntivo.to_excel('venditeConsuntivo.xlsx')

        return "OK"

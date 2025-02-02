import 'package:flutter/material.dart';
import 'package:frontendscg/database/constants.dart';
import 'package:frontendscg/screens/pagina%20secondaria/pagina_secondaria.dart';
import 'package:intl/intl.dart';

// Pulsante per accedere alle pagine secondarie degli scostamenti.
// Questo widget mostra anche il valore dello scostamento legato al pulsante

class PulsanteAltriScostamenti extends StatelessWidget {
  const PulsanteAltriScostamenti(
      {Key? key,
      required this.nomeScostamento,
      required this.dataPath,
      required this.graficoScostamentoData,
      required this.graficoBudgetConsuntivoData,
      required this.tabellaScostamenti,
      required this.tabellaValori,
      required this.valoreScostamento})
      : super(key: key);

  // Nome scostamento contenuto nel pulsante
  final String nomeScostamento;
  // Valore scostamento presente di fianco al pulsante
  final double valoreScostamento;
  // Nome chiave per accedere ai dati dentro la Map creata dall'api.
  final List<String> dataPath;

  // Function that returns data for the column graph
  final dynamic graficoScostamentoData;

  // Function that returns data for the column graph
  final dynamic graficoBudgetConsuntivoData;

  // Lista Dati della tabella scostamenti presente nella pagina secondaria
  final dynamic tabellaScostamenti;

  // Lista Dati della tabella valori presente nella pagina secondaria
  final dynamic tabellaValori;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 500,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Container(
            width: 200,
            padding: const EdgeInsets.only(right: 35),
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                primary: ColorData().pulsanti,
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) {
                      return PaginaSecondaria(
                        tabellaDatiScostamento: tabellaScostamenti,
                        tabellaDatiValori: tabellaValori,
                        graficoBudgetConsuntivoData:
                            graficoBudgetConsuntivoData,
                        graficoScostamentoData: graficoScostamentoData,
                        dataPath: dataPath,
                        titoloPagina: nomeScostamento,
                      );
                    },
                  ),
                );
              },
              child: Text(nomeScostamento),
            ),
          ),

          // Valore Scostamento
          Text(
            "€ ${NumberFormat.currency(name: "", decimalDigits: 0).format(valoreScostamento)} ",
            style: const TextStyle(fontSize: 30),
          ),
        ],
      ),
    );
  }
}

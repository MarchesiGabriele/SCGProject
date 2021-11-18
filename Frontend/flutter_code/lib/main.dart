import 'package:flutter/material.dart';
import 'package:frontendscg/graph_list_widget.dart';

void main() {
  runApp(const MyApp());
}

// Use this command to run the app on chrome
// flutter run -d chrome --web-renderer html

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SCGProject',
      home:  MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Progetto SCG"),
        centerTitle: true,
      ),
      body: const GraphListWidget()
      );
  }
}
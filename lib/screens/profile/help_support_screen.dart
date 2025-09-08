import 'package:flutter/material.dart';
import 'package:get/get.dart';

class HelpSupportScreen extends StatefulWidget {
  const HelpSupportScreen({super.key});

  @override
  State<HelpSupportScreen> createState() => _HelpSupportScreenState();
}

class _HelpSupportScreenState extends State<HelpSupportScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('HelpSupport'),
      ),
      body: Center(
        child: Text('HelpSupport - Coming Soon'),
      ),
    );
  }
}

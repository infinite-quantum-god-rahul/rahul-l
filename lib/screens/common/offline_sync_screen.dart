import 'package:flutter/material.dart';
import 'package:get/get.dart';

class OfflineSyncScreen extends StatefulWidget {
  const OfflineSyncScreen({super.key});

  @override
  State<OfflineSyncScreen> createState() => _OfflineSyncScreenState();
}

class _OfflineSyncScreenState extends State<OfflineSyncScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('OfflineSync'),
      ),
      body: Center(
        child: Text('OfflineSync - Coming Soon'),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';

import '../../config/app_theme.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';
import '../../utils/constants.dart';

class OfflineCapabilitiesScreen extends StatefulWidget {
  const OfflineCapabilitiesScreen({Key? key}) : super(key: key);

  @override
  State<OfflineCapabilitiesScreen> createState() => _OfflineCapabilitiesScreenState();
}

class _OfflineCapabilitiesScreenState extends State<OfflineCapabilitiesScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  bool _isOfflineMode = true;
  bool _isSyncing = false;
  int _pendingSyncCount = 0;
  int _localDataCount = 0;
  int _conflictCount = 0;
  List<Map<String, dynamic>> _offlineData = [];
  List<Map<String, dynamic>> _syncHistory = [];

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadOfflineData();
    _loadSyncHistory();
  }

  void _initializeAnimations() {
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));

    _animationController.forward();
  }

  void _loadOfflineData() {
    // Simulate loading offline data
    _offlineData = [
      {
        'id': 1,
        'type': 'client',
        'action': 'create',
        'data': {'name': 'John Doe', 'phone': '+91-9876543210'},
        'timestamp': DateTime.now().subtract(const Duration(hours: 2)),
        'status': 'pending',
      },
      {
        'id': 2,
        'type': 'loan',
        'action': 'update',
        'data': {'loanId': 'L001', 'status': 'approved'},
        'timestamp': DateTime.now().subtract(const Duration(hours: 1)),
        'status': 'pending',
      },
      {
        'id': 3,
        'type': 'field_visit',
        'action': 'create',
        'data': {'clientId': 'C001', 'visitDate': '2024-01-15'},
        'timestamp': DateTime.now().subtract(const Duration(minutes: 30)),
        'status': 'pending',
      },
    ];

    _localDataCount = _offlineData.length;
    _pendingSyncCount = _offlineData.where((item) => item['status'] == 'pending').length;
  }

  void _loadSyncHistory() {
    // Simulate loading sync history
    _syncHistory = [
      {
        'id': 1,
        'timestamp': DateTime.now().subtract(const Duration(days: 1)),
        'status': 'success',
        'itemsSynced': 15,
        'duration': '2m 30s',
      },
      {
        'id': 2,
        'timestamp': DateTime.now().subtract(const Duration(days: 2)),
        'status': 'success',
        'itemsSynced': 8,
        'duration': '1m 45s',
      },
      {
        'id': 3,
        'timestamp': DateTime.now().subtract(const Duration(days: 3)),
        'status': 'failed',
        'itemsSynced': 0,
        'duration': '0m 15s',
        'error': 'Network timeout',
      },
    ];
  }

  @override
  void dispose() {
    _animationController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        body: LoadingOverlay(
          isLoading: _isSyncing,
          child: Column(
            children: [
              _buildTabBar(),
              Expanded(
                child: TabBarView(
                  children: [
                    _buildOfflineStatusTab(),
                    _buildLocalDataTab(),
                    _buildSyncManagementTab(),
                    _buildBackupRestoreTab(),
                  ],
                ),
              ),
            ],
          ),
        ),
        floatingActionButton: _buildFloatingActionButton(),
      ),
    );
  }

  Widget _buildTabBar() {
    return Container(
      color: AppTheme.primaryColor,
      child: TabBar(
        labelColor: Colors.white,
        unselectedLabelColor: Colors.white70,
        indicatorColor: Colors.white,
        isScrollable: true,
        tabs: const [
          Tab(icon: Icon(Icons.offline_bolt), text: 'Status'),
          Tab(icon: Icon(Icons.storage), text: 'Local Data'),
          Tab(icon: Icon(Icons.sync), text: 'Sync'),
          Tab(icon: Icon(Icons.backup), text: 'Backup'),
        ],
      ),
    );
  }

  Widget _buildOfflineStatusTab() {
    return CustomScrollView(
      slivers: [
        _buildOfflineStatusHeader(),
        _buildOfflineStatusContent(),
        _buildNetworkStatus(),
        _buildOfflineCapabilities(),
      ],
    );
  }

  Widget _buildLocalDataTab() {
    return CustomScrollView(
      slivers: [
        _buildLocalDataHeader(),
        _buildLocalDataList(),
      ],
    );
  }

  Widget _buildSyncManagementTab() {
    return CustomScrollView(
      slivers: [
        _buildSyncManagementHeader(),
        _buildSyncControls(),
        _buildSyncHistory(),
      ],
    );
  }

  Widget _buildBackupRestoreTab() {
    return CustomScrollView(
      slivers: [
        _buildBackupRestoreHeader(),
        _buildBackupOptions(),
        _buildRestoreOptions(),
      ],
    );
  }

  Widget _buildOfflineStatusHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Offline Status', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.primaryGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Offline Mode', _isOfflineMode ? 'ON' : 'OFF', Icons.offline_bolt)),
                Expanded(child: _buildQuickStat('Pending Sync', '$_pendingSyncCount', Icons.pending)),
                Expanded(child: _buildQuickStat('Local Data', '$_localDataCount', Icons.storage)),
                Expanded(child: _buildQuickStat('Conflicts', '$_conflictCount', Icons.warning)),
              ],
            ),
          ),
        ),
      ),
      actions: [
        IconButton(icon: const Icon(Icons.settings, color: Colors.white), onPressed: _showOfflineSettings),
        IconButton(icon: const Icon(Icons.help, color: Colors.white), onPressed: _showOfflineHelp),
      ],
    );
  }

  Widget _buildLocalDataHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.secondaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Local Data', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.successGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Total Items', '$_localDataCount', Icons.inventory)),
                Expanded(child: _buildQuickStat('Pending', '$_pendingSyncCount', Icons.pending)),
                Expanded(child: _buildQuickStat('Synced', '${_localDataCount - _pendingSyncCount}', Icons.check_circle)),
                Expanded(child: _buildQuickStat('Size', '2.5 MB', Icons.storage)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSyncManagementHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.accentColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Sync Management', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.warningGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Last Sync', '2h ago', Icons.schedule)),
                Expanded(child: _buildQuickStat('Success Rate', '95%', Icons.trending_up)),
                Expanded(child: _buildQuickStat('Auto Sync', 'ON', Icons.auto_mode)),
                Expanded(child: _buildQuickStat('Sync Interval', '15m', Icons.timer)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildBackupRestoreHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.infoColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Backup & Restore', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.infoGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Last Backup', '1d ago', Icons.backup)),
                Expanded(child: _buildQuickStat('Backup Size', '15.2 MB', Icons.storage)),
                Expanded(child: _buildQuickStat('Auto Backup', 'ON', Icons.auto_mode)),
                Expanded(child: _buildQuickStat('Cloud Sync', 'ON', Icons.cloud_sync)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildQuickStat(String label, String value, IconData icon) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, color: Colors.white70, size: 20),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
      ],
    );
  }

  Widget _buildOfflineStatusContent() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Offline Status', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildStatusCard(),
            const SizedBox(height: 16),
            _buildOfflineModeToggle(),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusCard() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  _isOfflineMode ? Icons.offline_bolt : Icons.wifi,
                  color: _isOfflineMode ? AppTheme.warningColor : AppTheme.successColor,
                  size: 24,
                ),
                const SizedBox(width: 12),
                Text(
                  _isOfflineMode ? 'Offline Mode Active' : 'Online Mode Active',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: _isOfflineMode ? AppTheme.warningColor : AppTheme.successColor,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildStatusRow('Network Status', _isOfflineMode ? 'Disconnected' : 'Connected', _isOfflineMode ? Icons.signal_wifi_off : Icons.signal_wifi_4_bar),
            _buildStatusRow('Data Sync', _isOfflineMode ? 'Paused' : 'Active', _isOfflineMode ? Icons.pause : Icons.play_arrow),
            _buildStatusRow('Local Storage', 'Available', Icons.storage),
            _buildStatusRow('Last Sync', '2 hours ago', Icons.schedule),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusRow(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, color: Colors.grey[600], size: 20),
          const SizedBox(width: 12),
          Expanded(child: Text(label, style: const TextStyle(fontSize: 14))),
          Text(value, style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.grey[800])),
        ],
      ),
    );
  }

  Widget _buildOfflineModeToggle() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: SwitchListTile(
        title: const Text('Offline Mode', style: TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(_isOfflineMode ? 'App is working offline' : 'App is connected to server'),
        value: _isOfflineMode,
        onChanged: (value) {
          setState(() {
            _isOfflineMode = value;
          });
          _showOfflineModeChangeDialog(value);
        },
        secondary: Icon(
          _isOfflineMode ? Icons.offline_bolt : Icons.wifi,
          color: _isOfflineMode ? AppTheme.warningColor : AppTheme.successColor,
        ),
      ),
    );
  }

  Widget _buildNetworkStatus() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Network Status', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildNetworkCard(),
          ],
        ),
      ),
    );
  }

  Widget _buildNetworkCard() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _buildNetworkIndicator(),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: CustomButton(
                    text: 'Check Connection',
                    onPressed: _checkNetworkConnection,
                    icon: Icons.network_check,
                    style: CustomButtonStyle.secondary,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: CustomButton(
                    text: 'Test API',
                    onPressed: _testAPIConnection,
                    icon: Icons.api,
                    style: CustomButtonStyle.info,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNetworkIndicator() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: _isOfflineMode ? Colors.red[50] : Colors.green[50],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: _isOfflineMode ? Colors.red[200]! : Colors.green[200]!,
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            _isOfflineMode ? Icons.signal_wifi_off : Icons.signal_wifi_4_bar,
            color: _isOfflineMode ? Colors.red : Colors.green,
            size: 32,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _isOfflineMode ? 'No Internet Connection' : 'Internet Connected',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: _isOfflineMode ? Colors.red[700] : Colors.green[700],
                  ),
                ),
                Text(
                  _isOfflineMode ? 'Working in offline mode' : 'All features available',
                  style: TextStyle(
                    fontSize: 14,
                    color: _isOfflineMode ? Colors.red[600] : Colors.green[600],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildOfflineCapabilities() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Offline Capabilities', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildCapabilityCard('Data Entry', 'Create and edit clients, loans, and field visits', Icons.edit, true),
            const SizedBox(height: 8),
            _buildCapabilityCard('Document Management', 'Upload and manage KYC documents', Icons.description, true),
            const SizedBox(height: 8),
            _buildCapabilityCard('Field Operations', 'Record field visits and capture photos', Icons.visibility, true),
            const SizedBox(height: 8),
            _buildCapabilityCard('Offline Reports', 'View cached reports and analytics', Icons.analytics, true),
            const SizedBox(height: 8),
            _buildCapabilityCard('Data Sync', 'Automatic sync when connection restored', Icons.sync, true),
          ],
        ),
      ),
    );
  }

  Widget _buildCapabilityCard(String title, String description, IconData icon, bool available) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: available ? AppTheme.successColor.withOpacity(0.1) : Colors.grey.withOpacity(0.1),
          child: Icon(icon, color: available ? AppTheme.successColor : Colors.grey),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(description),
        trailing: Icon(
          available ? Icons.check_circle : Icons.cancel,
          color: available ? AppTheme.successColor : Colors.grey,
        ),
      ),
    );
  }

  Widget _buildLocalDataList() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Local Data Items', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _offlineData.length,
              itemBuilder: (context, index) {
                final item = _offlineData[index];
                return _buildLocalDataItem(item);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLocalDataItem(Map<String, dynamic> item) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _getItemTypeColor(item['type']).withOpacity(0.1),
          child: Icon(_getItemTypeIcon(item['type']), color: _getItemTypeColor(item['type'])),
        ),
        title: Text('${item['action'].toString().toUpperCase()} ${item['type'].toString().toUpperCase()}', style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Data: ${_formatItemData(item['data'])}'),
            Text('Status: ${item['status'].toString().toUpperCase()}'),
            Text('Time: ${_formatTimestamp(item['timestamp'])}'),
          ],
        ),
        trailing: PopupMenuButton(
          itemBuilder: (context) => [
            const PopupMenuItem(value: 'view', child: Text('View')),
            const PopupMenuItem(value: 'edit', child: Text('Edit')),
            const PopupMenuItem(value: 'delete', child: Text('Delete')),
            const PopupMenuItem(value: 'sync_now', child: Text('Sync Now')),
          ],
          onSelected: (value) => _handleLocalDataAction(value, item),
        ),
      ),
    );
  }

  Widget _buildSyncControls() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Sync Controls', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: CustomButton(
                    text: 'Sync Now',
                    onPressed: _startManualSync,
                    icon: Icons.sync,
                    style: CustomButtonStyle.primary,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: CustomButton(
                    text: 'Resolve Conflicts',
                    onPressed: _resolveConflicts,
                    icon: Icons.warning,
                    style: CustomButtonStyle.warning,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: CustomButton(
                    text: 'Clear Sync Queue',
                    onPressed: _clearSyncQueue,
                    icon: Icons.clear_all,
                    style: CustomButtonStyle.danger,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: CustomButton(
                    text: 'Sync Settings',
                    onPressed: _showSyncSettings,
                    icon: Icons.settings,
                    style: CustomButtonStyle.info,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSyncHistory() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Sync History', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _syncHistory.length,
              itemBuilder: (context, index) {
                final item = _syncHistory[index];
                return _buildSyncHistoryItem(item);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSyncHistoryItem(Map<String, dynamic> item) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _getSyncStatusColor(item['status']).withOpacity(0.1),
          child: Icon(_getSyncStatusIcon(item['status']), color: _getSyncStatusColor(item['status'])),
        ),
        title: Text('Sync ${item['id']}', style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Time: ${_formatTimestamp(item['timestamp'])}'),
            Text('Status: ${item['status'].toString().toUpperCase()}'),
            Text('Items: ${item['itemsSynced']} • Duration: ${item['duration']}'),
            if (item['error'] != null) Text('Error: ${item['error']}', style: TextStyle(color: AppTheme.errorColor)),
          ],
        ),
      ),
    );
  }

  Widget _buildBackupOptions() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Backup Options', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildBackupCard('Local Backup', 'Backup to device storage', Icons.phone_android, () => _createLocalBackup()),
            const SizedBox(height: 8),
            _buildBackupCard('Cloud Backup', 'Backup to Google Drive/OneDrive', Icons.cloud_upload, () => _createCloudBackup()),
            const SizedBox(height: 8),
            _buildBackupCard('Auto Backup', 'Automatic daily backup', Icons.auto_mode, () => _toggleAutoBackup()),
            const SizedBox(height: 8),
            _buildBackupCard('Encrypted Backup', 'Secure encrypted backup', Icons.security, () => _createEncryptedBackup()),
          ],
        ),
      ),
    );
  }

  Widget _buildBackupCard(String title, String description, IconData icon, VoidCallback onTap) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(icon, color: AppTheme.primaryColor, size: 24),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                    const SizedBox(height: 4),
                    Text(description, style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                  ],
                ),
              ),
              Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRestoreOptions() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Restore Options', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildRestoreCard('From Local Backup', 'Restore from device storage', Icons.phone_android, () => _restoreFromLocal()),
            const SizedBox(height: 8),
            _buildRestoreCard('From Cloud Backup', 'Restore from cloud storage', Icons.cloud_download, () => _restoreFromCloud()),
            const SizedBox(height: 8),
            _buildRestoreCard('Selective Restore', 'Restore specific data types', Icons.select_all, () => _selectiveRestore()),
            const SizedBox(height: 8),
            _buildRestoreCard('Factory Reset', 'Reset to default state', Icons.restore, () => _factoryReset()),
          ],
        ),
      ),
    );
  }

  Widget _buildRestoreCard(String title, String description, IconData icon, VoidCallback onTap) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(icon, color: AppTheme.secondaryColor, size: 24),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                    const SizedBox(height: 4),
                    Text(description, style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                  ],
                ),
              ),
              Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFloatingActionButton() {
    return FloatingActionButton.extended(
      onPressed: _showQuickActions,
      icon: const Icon(Icons.add),
      label: const Text('Quick Actions'),
      backgroundColor: AppTheme.primaryColor,
      foregroundColor: Colors.white,
    );
  }

  // Helper methods
  Color _getItemTypeColor(String type) {
    switch (type) {
      case 'client':
        return AppTheme.primaryColor;
      case 'loan':
        return AppTheme.secondaryColor;
      case 'field_visit':
        return AppTheme.accentColor;
      default:
        return Colors.grey;
    }
  }

  IconData _getItemTypeIcon(String type) {
    switch (type) {
      case 'client':
        return Icons.people;
      case 'loan':
        return Icons.account_balance;
      case 'field_visit':
        return Icons.visibility;
      default:
        return Icons.description;
    }
  }

  Color _getSyncStatusColor(String status) {
    switch (status) {
      case 'success':
        return AppTheme.successColor;
      case 'failed':
        return AppTheme.errorColor;
      case 'pending':
        return AppTheme.warningColor;
      default:
        return Colors.grey;
    }
  }

  IconData _getSyncStatusIcon(String status) {
    switch (status) {
      case 'success':
        return Icons.check_circle;
      case 'failed':
        return Icons.error;
      case 'pending':
        return Icons.pending;
      default:
        return Icons.help;
    }
  }

  String _formatItemData(Map<String, dynamic> data) {
    if (data.isEmpty) return 'No data';
    final firstKey = data.keys.first;
    return '${firstKey}: ${data[firstKey]}';
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);
    
    if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }

  // Event handlers
  void _showOfflineModeChangeDialog(bool isOffline) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(isOffline ? 'Enable Offline Mode' : 'Disable Offline Mode'),
        content: Text(isOffline 
          ? 'Offline mode will be enabled. Some features may be limited.'
          : 'Offline mode will be disabled. All features will be available.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(isOffline ? 'Offline mode enabled' : 'Offline mode disabled'),
                  backgroundColor: isOffline ? AppTheme.warningColor : AppTheme.successColor,
                ),
              );
            },
            child: const Text('Confirm'),
          ),
        ],
      ),
    );
  }

  void _checkNetworkConnection() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Checking network connection...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _testAPIConnection() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Testing API connection...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _handleLocalDataAction(String action, Map<String, dynamic> item) {
    switch (action) {
      case 'view':
        _viewLocalData(item);
        break;
      case 'edit':
        _editLocalData(item);
        break;
      case 'delete':
        _deleteLocalData(item);
        break;
      case 'sync_now':
        _syncItemNow(item);
        break;
    }
  }

  void _viewLocalData(Map<String, dynamic> item) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Viewing ${item['type']} data'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _editLocalData(Map<String, dynamic> item) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Editing ${item['type']} data'), backgroundColor: AppTheme.warningColor),
    );
  }

  void _deleteLocalData(Map<String, dynamic> item) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Local Data'),
        content: Text('Are you sure you want to delete this ${item['type']} data?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _offlineData.removeWhere((data) => data['id'] == item['id']);
                _localDataCount = _offlineData.length;
                _pendingSyncCount = _offlineData.where((data) => data['status'] == 'pending').length;
              });
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('${item['type']} data deleted'), backgroundColor: AppTheme.errorColor),
              );
            },
            child: const Text('Delete', style: TextStyle(color: AppTheme.errorColor)),
          ),
        ],
      ),
    );
  }

  void _syncItemNow(Map<String, dynamic> item) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Syncing ${item['type']} data...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _startManualSync() {
    setState(() {
      _isSyncing = true;
    });
    
    // Simulate sync process
    Future.delayed(const Duration(seconds: 3), () {
      setState(() {
        _isSyncing = false;
        _pendingSyncCount = 0;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Sync completed successfully'), backgroundColor: AppTheme.successColor),
      );
    });
  }

  void _resolveConflicts() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Opening conflict resolution...'), backgroundColor: AppTheme.warningColor),
    );
  }

  void _clearSyncQueue() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Clear Sync Queue'),
        content: const Text('Are you sure you want to clear all pending sync items?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _offlineData.clear();
                _localDataCount = 0;
                _pendingSyncCount = 0;
              });
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Sync queue cleared'), backgroundColor: AppTheme.errorColor),
              );
            },
            child: const Text('Clear', style: TextStyle(color: AppTheme.errorColor)),
          ),
        ],
      ),
    );
  }

  void _showSyncSettings() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Opening sync settings...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _createLocalBackup() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Creating local backup...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _createCloudBackup() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Creating cloud backup...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _toggleAutoBackup() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Toggling auto backup...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _createEncryptedBackup() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Creating encrypted backup...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _restoreFromLocal() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Restoring from local backup...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _restoreFromCloud() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Restoring from cloud backup...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _selectiveRestore() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Opening selective restore...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _factoryReset() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Factory Reset'),
        content: const Text('This will reset the app to its default state. All data will be lost. Are you sure?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Factory reset initiated'), backgroundColor: AppTheme.errorColor),
              );
            },
            child: const Text('Reset', style: TextStyle(color: AppTheme.errorColor)),
          ),
        ],
      ),
    );
  }

  void _showQuickActions() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildQuickActionsSheet(),
    );
  }

  Widget _buildQuickActionsSheet() {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Quick Actions', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close)),
              ],
            ),
            const SizedBox(height: 20),
            _buildQuickActionTile('Sync Now', Icons.sync, () { Navigator.pop(context); _startManualSync(); }),
            _buildQuickActionTile('Create Backup', Icons.backup, () { Navigator.pop(context); _createLocalBackup(); }),
            _buildQuickActionTile('Check Network', Icons.network_check, () { Navigator.pop(context); _checkNetworkConnection(); }),
            _buildQuickActionTile('Offline Settings', Icons.settings, () { Navigator.pop(context); _showOfflineSettings(); }),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickActionTile(String title, IconData icon, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primaryColor),
      title: Text(title),
      onTap: onTap,
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }

  void _showOfflineSettings() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Opening offline settings...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _showOfflineHelp() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Opening offline help...'), backgroundColor: AppTheme.infoColor),
    );
  }
}


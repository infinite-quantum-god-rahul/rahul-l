import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../config/app_theme.dart';
import '../../../widgets/common/loading_overlay.dart';

class FieldOperationsScreen extends StatefulWidget {
  const FieldOperationsScreen({Key? key}) : super(key: key);

  @override
  State<FieldOperationsScreen> createState() => _FieldOperationsScreenState();
}

class _FieldOperationsScreenState extends State<FieldOperationsScreen> {
  bool _isLoading = false;
  List<Map<String, dynamic>> _fieldVisits = [];
  List<Map<String, dynamic>> _fieldSchedules = [];

  @override
  void initState() {
    super.initState();
    _loadFieldData();
  }

  Future<void> _loadFieldData() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(seconds: 1));
      
      setState(() {
        _fieldVisits = [
          {
            'id': 'FV001',
            'clientName': 'Rahul Kumar',
            'village': 'Village Center #VC001',
            'visitDate': '2024-01-20',
            'status': 'Completed',
            'purpose': 'Loan Verification',
            'notes': 'Client verified successfully',
            'location': '12.9716° N, 77.5946° E',
          },
          {
            'id': 'FV002',
            'clientName': 'Priya Sharma',
            'village': 'Village Center #VC002',
            'visitDate': '2024-01-21',
            'status': 'Scheduled',
            'purpose': 'Collection Visit',
            'notes': 'Scheduled for payment collection',
            'location': '12.9716° N, 77.5946° E',
          },
          {
            'id': 'FV003',
            'clientName': 'Amit Patel',
            'village': 'Village Center #VC003',
            'visitDate': '2024-01-22',
            'status': 'Pending',
            'purpose': 'Field Investigation',
            'notes': 'Pending field investigation',
            'location': '12.9716° N, 77.5946° E',
          },
        ];

        _fieldSchedules = [
          {
            'id': 'FS001',
            'clientName': 'Priya Sharma',
            'village': 'Village Center #VC002',
            'scheduledDate': '2024-01-21',
            'time': '10:00 AM',
            'purpose': 'Collection Visit',
            'priority': 'High',
          },
          {
            'id': 'FS002',
            'clientName': 'Amit Patel',
            'village': 'Village Center #VC003',
            'scheduledDate': '2024-01-22',
            'time': '2:00 PM',
            'purpose': 'Field Investigation',
            'priority': 'Medium',
          },
          {
            'id': 'FS003',
            'clientName': 'Rajesh Kumar',
            'village': 'Village Center #VC004',
            'scheduledDate': '2024-01-23',
            'time': '11:00 AM',
            'purpose': 'Loan Verification',
            'priority': 'Low',
          },
        ];
      });
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to load field data: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: AppTheme.errorColor,
        colorText: Colors.white,
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Field Operations'),
          backgroundColor: AppTheme.primaryColor,
          foregroundColor: Colors.white,
          elevation: 0,
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Field Visits'),
              Tab(text: 'Schedules'),
            ],
            indicatorColor: Colors.white,
            labelColor: Colors.white,
            unselectedLabelColor: Colors.white70,
          ),
          actions: [
            IconButton(
              onPressed: () => _showMapView(),
              icon: const Icon(Icons.map),
            ),
            IconButton(
              onPressed: () => _showFilterDialog(),
              icon: const Icon(Icons.filter_list),
            ),
          ],
        ),
        body: LoadingOverlay(
          isLoading: _isLoading,
          child: TabBarView(
            children: [
              _buildFieldVisitsTab(),
              _buildSchedulesTab(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFieldVisitsTab() {
    return RefreshIndicator(
      onRefresh: _loadFieldData,
      child: _fieldVisits.isEmpty && !_isLoading
          ? _buildEmptyState('Field Visits', 'No field visits found')
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _fieldVisits.length,
              itemBuilder: (context, index) {
                final visit = _fieldVisits[index];
                return _buildFieldVisitCard(visit);
              },
            ),
    );
  }

  Widget _buildSchedulesTab() {
    return RefreshIndicator(
      onRefresh: _loadFieldData,
      child: _fieldSchedules.isEmpty && !_isLoading
          ? _buildEmptyState('Schedules', 'No field schedules found')
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _fieldSchedules.length,
              itemBuilder: (context, index) {
                final schedule = _fieldSchedules[index];
                return _buildScheduleCard(schedule);
              },
            ),
    );
  }

  Widget _buildEmptyState(String title, String message) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.location_on_outlined,
            size: 80,
            color: AppTheme.textSecondaryColor.withOpacity(0.5),
          ),
          const SizedBox(height: 16),
          Text(
            title,
            style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
              color: AppTheme.textSecondaryColor,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            message,
            style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
              color: AppTheme.textSecondaryColor.withOpacity(0.7),
            ),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () => _addNewFieldVisit(),
            icon: const Icon(Icons.add),
            label: const Text('Add Field Visit'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(
                horizontal: 24,
                vertical: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFieldVisitCard(Map<String, dynamic> visit) {
    final statusColor = _getStatusColor(visit['status']);

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Visit #${visit['id']}',
                        style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      Text(
                        visit['clientName'],
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: statusColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: statusColor.withOpacity(0.3),
                    ),
                  ),
                  child: Text(
                    visit['status'],
                    style: AppTheme.lightTheme.textTheme.labelSmall?.copyWith(
                      color: statusColor,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Details
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Village',
                        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                      Text(
                        visit['village'],
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Date',
                        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                      Text(
                        visit['visitDate'],
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Purpose and Notes
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Purpose',
                  style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                    color: AppTheme.textSecondaryColor,
                  ),
                ),
                Text(
                  visit['purpose'],
                  style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w500,
                  ),
                ),
                if (visit['notes'] != null) ...[
                  const SizedBox(height: 8),
                  Text(
                    'Notes',
                    style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                      color: AppTheme.textSecondaryColor,
                    ),
                  ),
                  Text(
                    visit['notes'],
                    style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                      color: AppTheme.textSecondaryColor,
                    ),
                  ),
                ],
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Actions
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => _viewVisitDetails(visit),
                    icon: const Icon(Icons.visibility, size: 16),
                    label: const Text('View'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: AppTheme.primaryColor,
                      side: BorderSide(color: AppTheme.primaryColor),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => _editVisit(visit),
                    icon: const Icon(Icons.edit, size: 16),
                    label: const Text('Edit'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.warningColor,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildScheduleCard(Map<String, dynamic> schedule) {
    final priorityColor = _getPriorityColor(schedule['priority']);

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Schedule #${schedule['id']}',
                        style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      Text(
                        schedule['clientName'],
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: priorityColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: priorityColor.withOpacity(0.3),
                    ),
                  ),
                  child: Text(
                    schedule['priority'],
                    style: AppTheme.lightTheme.textTheme.labelSmall?.copyWith(
                      color: priorityColor,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Details
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Village',
                        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                      Text(
                        schedule['village'],
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Date & Time',
                        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                      Text(
                        '${schedule['scheduledDate']}\n${schedule['time']}',
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Purpose
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Purpose',
                  style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                    color: AppTheme.textSecondaryColor,
                  ),
                ),
                Text(
                  schedule['purpose'],
                  style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Actions
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => _viewScheduleDetails(schedule),
                    icon: const Icon(Icons.visibility, size: 16),
                    label: const Text('View'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: AppTheme.primaryColor,
                      side: BorderSide(color: AppTheme.primaryColor),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => _startFieldVisit(schedule),
                    icon: const Icon(Icons.play_arrow, size: 16),
                    label: const Text('Start Visit'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.successColor,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'completed':
        return AppTheme.successColor;
      case 'scheduled':
        return AppTheme.infoColor;
      case 'pending':
        return AppTheme.warningColor;
      case 'cancelled':
        return AppTheme.errorColor;
      default:
        return AppTheme.textSecondaryColor;
    }
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'high':
        return AppTheme.errorColor;
      case 'medium':
        return AppTheme.warningColor;
      case 'low':
        return AppTheme.successColor;
      default:
        return AppTheme.textSecondaryColor;
    }
  }

  void _addNewFieldVisit() {
    Get.snackbar(
      'Add Field Visit',
      'Add field visit functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _viewVisitDetails(Map<String, dynamic> visit) {
    Get.snackbar(
      'View Visit',
      'Viewing details for visit #${visit['id']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _editVisit(Map<String, dynamic> visit) {
    Get.snackbar(
      'Edit Visit',
      'Editing visit #${visit['id']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _viewScheduleDetails(Map<String, dynamic> schedule) {
    Get.snackbar(
      'View Schedule',
      'Viewing details for schedule #${schedule['id']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _startFieldVisit(Map<String, dynamic> schedule) {
    Get.snackbar(
      'Start Visit',
      'Starting field visit for schedule #${schedule['id']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showMapView() {
    Get.snackbar(
      'Map View',
      'Map view functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showFilterDialog() {
    Get.snackbar(
      'Filter',
      'Filter functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }
}


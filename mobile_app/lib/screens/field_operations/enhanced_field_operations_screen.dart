import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:geolocator/geolocator.dart';

import '../../config/app_theme.dart';
import '../../models/sml_models.dart';
import '../../providers/sml_providers.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';
import '../../utils/constants.dart';

class EnhancedFieldOperationsScreen extends StatefulWidget {
  const EnhancedFieldOperationsScreen({Key? key}) : super(key: key);

  @override
  State<EnhancedFieldOperationsScreen> createState() => _EnhancedFieldOperationsScreenState();
}

class _EnhancedFieldOperationsScreenState extends State<EnhancedFieldOperationsScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  String _selectedFilter = 'all';
  String _selectedSortBy = 'scheduled_date';
  String _selectedSortOrder = 'asc';

  Position? _currentPosition;
  bool _isLocationEnabled = false;

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadInitialData();
    _setupScrollListener();
    _checkLocationPermission();
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

  void _loadInitialData() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SMLFieldOperationsProvider>().loadFieldVisits();
    });
  }

  void _setupScrollListener() {
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >=
          _scrollController.position.maxScrollExtent - 200) {
        _loadMoreData();
      }
    });
  }

  void _loadMoreData() {
    final provider = context.read<SMLFieldOperationsProvider>();
    if (provider.hasMoreData && !provider.isLoading) {
      provider.loadMoreFieldVisits();
    }
  }

  Future<void> _checkLocationPermission() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        setState(() {
          _isLocationEnabled = false;
        });
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          setState(() {
            _isLocationEnabled = false;
          });
          return;
        }
      }

      setState(() {
        _isLocationEnabled = true;
      });

      _getCurrentLocation();
    } catch (e) {
      setState(() {
        _isLocationEnabled = false;
      });
    }
  }

  Future<void> _getCurrentLocation() async {
    try {
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        _currentPosition = position;
      });
    } catch (e) {
      // Handle location error
    }
  }

  @override
  void dispose() {
    _animationController.dispose();
    _searchController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        body: LoadingOverlay(
          isLoading: context.watch<SMLFieldOperationsProvider>().isLoading,
          child: Column(
            children: [
              _buildTabBar(),
              Expanded(
                child: TabBarView(
                  children: [
                    _buildFieldVisitsTab(),
                    _buildFieldSchedulesTab(),
                    _buildFieldReportsTab(),
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
        tabs: const [
          Tab(icon: Icon(Icons.visibility), text: 'Field Visits'),
          Tab(icon: Icon(Icons.schedule), text: 'Schedules'),
          Tab(icon: Icon(Icons.analytics), text: 'Reports'),
        ],
      ),
    );
  }

  Widget _buildFieldVisitsTab() {
    return CustomScrollView(
      controller: _scrollController,
      slivers: [
        _buildFieldVisitsHeader(),
        _buildSearchAndFilters(),
        _buildFieldVisitsList(),
      ],
    );
  }

  Widget _buildFieldSchedulesTab() {
    return CustomScrollView(
      slivers: [
        _buildFieldSchedulesHeader(),
        _buildFieldSchedulesList(),
      ],
    );
  }

  Widget _buildFieldReportsTab() {
    return CustomScrollView(
      slivers: [
        _buildFieldReportsHeader(),
        _buildFieldReportsContent(),
      ],
    );
  }

  Widget _buildFieldVisitsHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Field Visits', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.primaryGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Total Visits', '0', Icons.visibility)),
                Expanded(child: _buildQuickStat('Completed', '0', Icons.check_circle)),
                Expanded(child: _buildQuickStat('Pending', '0', Icons.pending)),
                Expanded(child: _buildQuickStat('Overdue', '0', Icons.warning)),
              ],
            ),
          ),
        ),
      ),
      actions: [
        IconButton(icon: const Icon(Icons.filter_list, color: Colors.white), onPressed: _showAdvancedFilters),
        IconButton(icon: const Icon(Icons.more_vert, color: Colors.white), onPressed: _showMoreOptions),
      ],
    );
  }

  Widget _buildFieldSchedulesHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.secondaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Field Schedules', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.successGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Total Schedules', '0', Icons.schedule)),
                Expanded(child: _buildQuickStat('Today', '0', Icons.today)),
                Expanded(child: _buildQuickStat('This Week', '0', Icons.view_week)),
                Expanded(child: _buildQuickStat('This Month', '0', Icons.calendar_month)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFieldReportsHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.accentColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Field Reports', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.warningGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Visit Reports', '0', Icons.assessment)),
                Expanded(child: _buildQuickStat('Performance', '0', Icons.trending_up)),
                Expanded(child: _buildQuickStat('Analytics', '0', Icons.analytics)),
                Expanded(child: _buildQuickStat('Export', '0', Icons.file_download)),
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

  Widget _buildSearchAndFilters() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _buildSearchBar(),
            const SizedBox(height: 16),
            _buildQuickFilters(),
            const SizedBox(height: 16),
            _buildLocationStatus(),
          ],
        ),
      ),
    );
  }

  Widget _buildSearchBar() {
    return CustomTextField(
      controller: _searchController,
      hintText: 'Search field visits by client name, purpose...',
      prefixIcon: Icons.search,
      onChanged: _onSearchChanged,
      suffixIcon: _searchController.text.isNotEmpty ? Icons.clear : null,
      onSuffixIconPressed: _clearSearch,
    );
  }

  Widget _buildQuickFilters() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: [
          _buildFilterChip('All', 'all'),
          const SizedBox(width: 8),
          _buildFilterChip('Completed', 'completed'),
          const SizedBox(width: 8),
          _buildFilterChip('Pending', 'pending'),
          const SizedBox(width: 8),
          _buildFilterChip('In Progress', 'in_progress'),
          const SizedBox(width: 8),
          _buildFilterChip('Overdue', 'overdue'),
        ],
      ),
    );
  }

  Widget _buildLocationStatus() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: _isLocationEnabled ? Colors.green[50] : Colors.red[50],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: _isLocationEnabled ? Colors.green : Colors.red, width: 1),
      ),
      child: Row(
        children: [
          Icon(_isLocationEnabled ? Icons.location_on : Icons.location_off, 
               color: _isLocationEnabled ? Colors.green : Colors.red),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              _isLocationEnabled ? 'Location tracking enabled' : 'Location tracking disabled',
              style: TextStyle(
                color: _isLocationEnabled ? Colors.green[700] : Colors.red[700],
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          if (!_isLocationEnabled)
            TextButton(onPressed: _checkLocationPermission, child: const Text('Enable')),
        ],
      ),
    );
  }

  Widget _buildFilterChip(String label, String value) {
    final isSelected = _selectedFilter == value;
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) => _onFilterChanged(value),
      selectedColor: AppTheme.primaryColor.withOpacity(0.2),
      checkmarkColor: AppTheme.primaryColor,
      backgroundColor: Colors.grey[200],
      labelStyle: TextStyle(
        color: isSelected ? AppTheme.primaryColor : Colors.black87,
        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
      ),
    );
  }

  Widget _buildFieldVisitsList() {
    return Consumer<SMLFieldOperationsProvider>(
      builder: (context, provider, child) {
        if (provider.fieldVisits.isEmpty && !provider.isLoading) {
          return _buildEmptyState();
        }

        return SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              if (index >= provider.fieldVisits.length) {
                if (provider.hasMoreData) {
                  return _buildLoadingMore();
                }
                return const SizedBox.shrink();
              }

              final visit = provider.fieldVisits[index];
              return _buildFieldVisitCard(visit);
            },
            childCount: provider.fieldVisits.length + (provider.hasMoreData ? 1 : 0),
          ),
        );
      },
    );
  }

  Widget _buildFieldSchedulesList() {
    return Consumer<SMLFieldOperationsProvider>(
      builder: (context, provider, child) {
        if (provider.fieldSchedules.isEmpty && !provider.isLoading) {
          return _buildEmptySchedulesState();
        }

        return SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              final schedule = provider.fieldSchedules[index];
              return _buildFieldScheduleCard(schedule);
            },
            childCount: provider.fieldSchedules.length,
          ),
        );
      },
    );
  }

  Widget _buildFieldReportsContent() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildReportCard('Visit Completion Report', 'Track field visit completion rates', Icons.assessment, () => _generateVisitReport()),
            const SizedBox(height: 16),
            _buildReportCard('Field Performance Analytics', 'Analyze field staff performance', Icons.analytics, () => _generatePerformanceReport()),
            const SizedBox(height: 16),
            _buildReportCard('Geographic Coverage Report', 'View field coverage by location', Icons.map, () => _generateCoverageReport()),
            const SizedBox(height: 16),
            _buildReportCard('Client Visit History', 'Track client visit patterns', Icons.history, () => _generateClientHistoryReport()),
          ],
        ),
      ),
    );
  }

  Widget _buildReportCard(String title, String description, IconData icon, VoidCallback onTap) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppTheme.primaryColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(icon, color: AppTheme.primaryColor, size: 24),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87)),
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

  Widget _buildFieldVisitCard(SMLFieldVisit visit) {
    return FadeTransition(
      opacity: _fadeAnimation,
      child: SlideTransition(
        position: _slideAnimation,
        child: Card(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          elevation: 4,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: InkWell(
            onTap: () => _onFieldVisitTap(visit),
            borderRadius: BorderRadius.circular(12),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(visit.visitCode ?? 'N/A', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87)),
                            const SizedBox(height: 4),
                            Text('Client: ${visit.clientName ?? 'N/A'}', style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                          ],
                        ),
                      ),
                      _buildVisitStatusChip(visit.status),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(child: _buildVisitInfo('Purpose', visit.purpose ?? 'N/A', Icons.assignment)),
                      Expanded(child: _buildVisitInfo('Priority', visit.priority ?? 'N/A', Icons.priority_high)),
                      Expanded(child: _buildVisitInfo('Type', visit.visitType ?? 'N/A', Icons.category)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(child: _buildVisitInfo('Scheduled', visit.formattedScheduledDate, Icons.schedule)),
                      Expanded(child: _buildVisitInfo('Actual', visit.formattedActualDate ?? 'Not completed', Icons.check_circle)),
                      Expanded(child: _buildVisitInfo('Location', visit.location ?? 'N/A', Icons.location_on)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildActionButton('View Details', Icons.visibility, () => _onViewVisitDetails(visit), AppTheme.primaryColor),
                      _buildActionButton('Start Visit', Icons.play_arrow, () => _onStartVisit(visit), AppTheme.successColor),
                      _buildActionButton('Complete', Icons.check, () => _onCompleteVisit(visit), AppTheme.accentColor),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFieldScheduleCard(SMLFieldSchedule schedule) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(schedule.scheduleCode ?? 'N/A', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87)),
                      const SizedBox(height: 4),
                      Text('Client: ${schedule.clientName ?? 'N/A'}', style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                    ],
                  ),
                ),
                _buildScheduleStatusChip(schedule.status),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(child: _buildScheduleInfo('Date', schedule.formattedScheduledDate, Icons.calendar_today)),
                Expanded(child: _buildScheduleInfo('Time', schedule.formattedScheduledTime, Icons.access_time)),
                Expanded(child: _buildScheduleInfo('Priority', schedule.priority ?? 'N/A', Icons.priority_high)),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(child: _buildScheduleInfo('Purpose', schedule.purpose ?? 'N/A', Icons.assignment)),
                Expanded(child: _buildScheduleInfo('Location', schedule.location ?? 'N/A', Icons.location_on)),
                Expanded(child: _buildScheduleInfo('Type', schedule.visitType ?? 'N/A', Icons.category)),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildActionButton('View Details', Icons.visibility, () => _onViewScheduleDetails(schedule), AppTheme.primaryColor),
                _buildActionButton('Start Visit', Icons.play_arrow, () => _onStartScheduledVisit(schedule), AppTheme.successColor),
                _buildActionButton('Reschedule', Icons.schedule, () => _onReschedule(schedule), AppTheme.warningColor),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildVisitStatusChip(String status) {
    Color color;
    IconData icon;

    switch (status.toLowerCase()) {
      case 'completed':
        color = AppTheme.successColor;
        icon = Icons.check_circle;
        break;
      case 'pending':
        color = AppTheme.warningColor;
        icon = Icons.pending;
        break;
      case 'in_progress':
        color = AppTheme.infoColor;
        icon = Icons.play_arrow;
        break;
      case 'overdue':
        color = AppTheme.errorColor;
        icon = Icons.warning;
        break;
      default:
        color = Colors.grey;
        icon = Icons.help;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: color),
          const SizedBox(width: 4),
          Text(status.toUpperCase(), style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }

  Widget _buildScheduleStatusChip(String status) {
    Color color;
    IconData icon;

    switch (status.toLowerCase()) {
      case 'scheduled':
        color = AppTheme.infoColor;
        icon = Icons.schedule;
        break;
      case 'in_progress':
        color = AppTheme.warningColor;
        icon = Icons.play_arrow;
        break;
      case 'completed':
        color = AppTheme.successColor;
        icon = Icons.check_circle;
        break;
      case 'cancelled':
        color = AppTheme.errorColor;
        icon = Icons.cancel;
        break;
      default:
        color = Colors.grey;
        icon = Icons.help;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: color),
          const SizedBox(width: 4),
          Text(status.toUpperCase(), style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }

  Widget _buildVisitInfo(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, size: 20, color: AppTheme.primaryColor),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.black87), textAlign: TextAlign.center, maxLines: 2, overflow: TextOverflow.ellipsis),
        Text(label, style: TextStyle(fontSize: 12, color: Colors.grey[600]), textAlign: TextAlign.center),
      ],
    );
  }

  Widget _buildScheduleInfo(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, size: 20, color: AppTheme.secondaryColor),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.black87), textAlign: TextAlign.center, maxLines: 2, overflow: TextOverflow.ellipsis),
        Text(label, style: TextStyle(fontSize: 12, color: Colors.grey[600]), textAlign: TextAlign.center),
      ],
    );
  }

  Widget _buildActionButton(String text, IconData icon, VoidCallback onPressed, Color color) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4),
        child: ElevatedButton.icon(
          onPressed: onPressed,
          icon: Icon(icon, size: 16),
          label: Text(text, style: const TextStyle(fontSize: 12)),
          style: ElevatedButton.styleFrom(
            backgroundColor: color,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 8),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return SliverFillRemaining(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.visibility_outlined, size: 80, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text('No Field Visits Found', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.grey[600])),
            const SizedBox(height: 8),
            Text('Start by creating your first field visit', style: TextStyle(fontSize: 16, color: Colors.grey[500]), textAlign: TextAlign.center),
            const SizedBox(height: 24),
            CustomButton(text: 'Add Field Visit', onPressed: _onAddFieldVisit, icon: Icons.add, style: CustomButtonStyle.primary),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptySchedulesState() {
    return SliverFillRemaining(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.schedule_outlined, size: 80, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text('No Field Schedules Found', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.grey[600])),
            const SizedBox(height: 8),
            Text('Start by creating your first field schedule', style: TextStyle(fontSize: 16, color: Colors.grey[500]), textAlign: TextAlign.center),
            const SizedBox(height: 24),
            CustomButton(text: 'Add Field Schedule', onPressed: _onAddFieldSchedule, icon: Icons.add, style: CustomButtonStyle.primary),
          ],
        ),
      ),
    );
  }

  Widget _buildLoadingMore() {
    return const Padding(
      padding: EdgeInsets.all(16),
      child: Center(child: CircularProgressIndicator()),
    );
  }

  Widget _buildFloatingActionButton() {
    return FloatingActionButton.extended(
      onPressed: _onAddFieldVisit,
      icon: const Icon(Icons.add),
      label: const Text('Add Visit'),
      backgroundColor: AppTheme.primaryColor,
      foregroundColor: Colors.white,
    );
  }

  // Event handlers
  void _onSearchChanged(String query) => context.read<SMLFieldOperationsProvider>().searchFieldVisits(query);
  void _clearSearch() { _searchController.clear(); context.read<SMLFieldOperationsProvider>().clearSearch(); }
  void _onFilterChanged(String filter) { setState(() { _selectedFilter = filter; }); context.read<SMLFieldOperationsProvider>().filterFieldVisitsByStatus(filter); }
  void _onFieldVisitTap(SMLFieldVisit visit) => Get.toNamed('/field-visit-details', arguments: visit);
  void _onViewVisitDetails(SMLFieldVisit visit) => Get.toNamed('/field-visit-details', arguments: visit);
  void _onStartVisit(SMLFieldVisit visit) => Get.toNamed('/start-field-visit', arguments: visit);
  void _onCompleteVisit(SMLFieldVisit visit) => Get.toNamed('/complete-field-visit', arguments: visit);
  void _onViewScheduleDetails(SMLFieldSchedule schedule) => Get.toNamed('/field-schedule-details', arguments: schedule);
  void _onStartScheduledVisit(SMLFieldSchedule schedule) => Get.toNamed('/start-scheduled-visit', arguments: schedule);
  void _onReschedule(SMLFieldSchedule schedule) => Get.toNamed('/reschedule-field-visit', arguments: schedule);
  void _onAddFieldVisit() => Get.toNamed('/add-field-visit');
  void _onAddFieldSchedule() => Get.toNamed('/add-field-schedule');
  void _generateVisitReport() => Get.toNamed('/visit-report');
  void _generatePerformanceReport() => Get.toNamed('/performance-report');
  void _generateCoverageReport() => Get.toNamed('/coverage-report');
  void _generateClientHistoryReport() => Get.toNamed('/client-history-report');

  void _showAdvancedFilters() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildAdvancedFiltersSheet(),
    );
  }

  Widget _buildAdvancedFiltersSheet() {
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
                const Text('Advanced Filters', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close)),
              ],
            ),
            const SizedBox(height: 20),
            const Text('Sort By', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                _buildChoiceChip('Scheduled Date', 'scheduled_date'),
                _buildChoiceChip('Priority', 'priority'),
                _buildChoiceChip('Client Name', 'client_name'),
                _buildChoiceChip('Status', 'status'),
              ],
            ),
            const SizedBox(height: 20),
            const Text('Sort Order', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                _buildChoiceChip('Ascending', 'asc'),
                _buildChoiceChip('Descending', 'desc'),
              ],
            ),
            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              child: CustomButton(
                text: 'Apply Filters',
                onPressed: () { _applyAdvancedFilters(); Navigator.pop(context); },
                style: CustomButtonStyle.primary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChoiceChip(String label, String value) {
    bool isSelected = false;
    if (label.contains('Scheduled Date') || label.contains('scheduled_date')) {
      isSelected = _selectedSortBy == 'scheduled_date';
    } else if (label.contains('Ascending') || label.contains('asc')) {
      isSelected = _selectedSortOrder == 'asc';
    }

    return ChoiceChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        setState(() {
          if (label.contains('Scheduled Date') || label.contains('scheduled_date')) {
            _selectedSortBy = value;
          } else if (label.contains('Ascending') || label.contains('asc')) {
            _selectedSortOrder = value;
          }
        });
      },
      selectedColor: AppTheme.primaryColor.withOpacity(0.2),
      checkmarkColor: AppTheme.primaryColor,
      backgroundColor: Colors.grey[200],
      labelStyle: TextStyle(
        color: isSelected ? AppTheme.primaryColor : Colors.black87,
        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
      ),
    );
  }

  void _applyAdvancedFilters() {
    final provider = context.read<SMLFieldOperationsProvider>();
    provider.filterFieldVisits(sortBy: _selectedSortBy, sortOrder: _selectedSortOrder);
  }

  void _showMoreOptions() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildMoreOptionsSheet(),
    );
  }

  Widget _buildMoreOptionsSheet() {
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
                const Text('More Options', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close)),
              ],
            ),
            const SizedBox(height: 20),
            _buildOptionTile('Export Field Data', Icons.file_download, () { Navigator.pop(context); _exportFieldData(); }),
            _buildOptionTile('Field Operations Settings', Icons.settings, () { Navigator.pop(context); _openFieldSettings(); }),
            _buildOptionTile('Help & Support', Icons.help, () { Navigator.pop(context); _openHelpSupport(); }),
            _buildOptionTile('About Field Operations', Icons.info, () { Navigator.pop(context); _showAboutFieldOperations(); }),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionTile(String title, IconData icon, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primaryColor),
      title: Text(title),
      onTap: onTap,
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }

  void _exportFieldData() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Export functionality coming soon!'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _openFieldSettings() => Get.toNamed('/field-settings');
  void _openHelpSupport() => Get.toNamed('/help-support');

  void _showAboutFieldOperations() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('About Field Operations'),
        content: const Text('This module provides comprehensive field operations management including visit scheduling, GPS tracking, and performance analytics.'),
        actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text('OK'))],
      ),
    );
  }
}

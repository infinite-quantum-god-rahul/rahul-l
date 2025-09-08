import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import '../../config/app_theme.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';

class MultiLanguageSupportScreen extends StatefulWidget {
  const MultiLanguageSupportScreen({Key? key}) : super(key: key);

  @override
  State<MultiLanguageSupportScreen> createState() => _MultiLanguageSupportScreenState();
}

class _MultiLanguageSupportScreenState extends State<MultiLanguageSupportScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  String _selectedLanguage = 'en';
  String _selectedRegion = 'IN';
  bool _isVoiceNavigationEnabled = false;
  bool _isHighContrastEnabled = false;
  bool _isLargeTextEnabled = false;
  bool _isReducedMotionEnabled = false;

  final Map<String, Map<String, String>> _languages = {
    'en': {
      'name': 'English',
      'native': 'English',
      'flag': '🇺🇸',
      'direction': 'ltr',
    },
    'hi': {
      'name': 'Hindi',
      'native': 'हिंदी',
      'flag': '🇮🇳',
      'direction': 'ltr',
    },
    'kn': {
      'name': 'Kannada',
      'native': 'ಕನ್ನಡ',
      'flag': '🇮🇳',
      'direction': 'ltr',
    },
  };

  final Map<String, Map<String, String>> _regions = {
    'IN': {
      'name': 'India',
      'flag': '🇮🇳',
      'currency': '₹',
      'dateFormat': 'dd/MM/yyyy',
    },
    'US': {
      'name': 'United States',
      'flag': '🇺🇸',
      'currency': '\$',
      'dateFormat': 'MM/dd/yyyy',
    },
    'UK': {
      'name': 'United Kingdom',
      'flag': '🇬🇧',
      'currency': '£',
      'dateFormat': 'dd/MM/yyyy',
    },
  };

  final List<Map<String, dynamic>> _accessibilityFeatures = [
    {
      'id': 'voice_navigation',
      'title': 'Voice Navigation',
      'description': 'Navigate the app using voice commands',
      'icon': Icons.record_voice_over,
      'enabled': false,
    },
    {
      'id': 'high_contrast',
      'title': 'High Contrast',
      'description': 'Increase contrast for better visibility',
      'icon': Icons.contrast,
      'enabled': false,
    },
    {
      'id': 'large_text',
      'title': 'Large Text',
      'description': 'Increase text size for better readability',
      'icon': Icons.text_fields,
      'enabled': false,
    },
    {
      'id': 'reduced_motion',
      'title': 'Reduced Motion',
      'description': 'Reduce animations for motion sensitivity',
      'icon': Icons.motion_photos_pause,
      'enabled': false,
    },
    {
      'id': 'screen_reader',
      'title': 'Screen Reader',
      'description': 'Enable screen reader support',
      'icon': Icons.accessibility,
      'enabled': false,
    },
  ];

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadCurrentSettings();
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

  void _loadCurrentSettings() {
    // Load current language and region settings
    // This would typically come from SharedPreferences or app state
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
      length: 3,
      child: Scaffold(
        body: LoadingOverlay(
          isLoading: false,
          child: Column(
            children: [
              _buildTabBar(),
              Expanded(
                child: TabBarView(
                  children: [
                    _buildLanguageTab(),
                    _buildRegionalTab(),
                    _buildAccessibilityTab(),
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
          Tab(icon: Icon(Icons.language), text: 'Language'),
          Tab(icon: Icon(Icons.public), text: 'Regional'),
          Tab(icon: Icon(Icons.accessibility), text: 'Accessibility'),
        ],
      ),
    );
  }

  Widget _buildLanguageTab() {
    return CustomScrollView(
      slivers: [
        _buildLanguageHeader(),
        _buildLanguageList(),
        _buildLanguageSettings(),
      ],
    );
  }

  Widget _buildRegionalTab() {
    return CustomScrollView(
      slivers: [
        _buildRegionalHeader(),
        _buildRegionalSettings(),
        _buildCulturalAdaptations(),
      ],
    );
  }

  Widget _buildAccessibilityTab() {
    return CustomScrollView(
      slivers: [
        _buildAccessibilityHeader(),
        _buildAccessibilityFeatures(),
        _buildVoiceNavigationSettings(),
      ],
    );
  }

  Widget _buildLanguageHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Language Settings', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.primaryGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Current', _languages[_selectedLanguage]?['name'] ?? 'English', Icons.language)),
                Expanded(child: _buildQuickStat('Available', '${_languages.length}', Icons.list)),
                Expanded(child: _buildQuickStat('Direction', _languages[_selectedLanguage]?['direction']?.toUpperCase() ?? 'LTR', Icons.text_direction)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRegionalHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.secondaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Regional Settings', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.successGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Region', _regions[_selectedRegion]?['name'] ?? 'India', Icons.public)),
                Expanded(child: _buildQuickStat('Currency', _regions[_selectedRegion]?['currency'] ?? '₹', Icons.attach_money)),
                Expanded(child: _buildQuickStat('Date Format', _regions[_selectedRegion]?['dateFormat'] ?? 'dd/MM/yyyy', Icons.date_range)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildAccessibilityHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.accentColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Accessibility', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.warningGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Features', '${_accessibilityFeatures.length}', Icons.accessibility)),
                Expanded(child: _buildQuickStat('Voice Nav', _isVoiceNavigationEnabled ? 'ON' : 'OFF', Icons.record_voice_over)),
                Expanded(child: _buildQuickStat('High Contrast', _isHighContrastEnabled ? 'ON' : 'OFF', Icons.contrast)),
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

  Widget _buildLanguageList() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Available Languages', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _languages.length,
              itemBuilder: (context, index) {
                final languageCode = _languages.keys.elementAt(index);
                final language = _languages[languageCode]!;
                return _buildLanguageCard(languageCode, language);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLanguageCard(String languageCode, Map<String, String> language) {
    final isSelected = _selectedLanguage == languageCode;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: isSelected ? 4 : 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: () => _selectLanguage(languageCode),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isSelected ? AppTheme.primaryColor : Colors.transparent,
              width: 2,
            ),
          ),
          child: Row(
            children: [
              Text(
                language['flag']!,
                style: const TextStyle(fontSize: 32),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      language['name']!,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: isSelected ? AppTheme.primaryColor : Colors.black87,
                      ),
                    ),
                    Text(
                      language['native']!,
                      style: TextStyle(
                        fontSize: 16,
                        color: isSelected ? AppTheme.primaryColor : Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ),
              if (isSelected)
                Icon(
                  Icons.check_circle,
                  color: AppTheme.primaryColor,
                  size: 24,
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLanguageSettings() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Language Settings', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildSettingCard(
              'Auto-detect Language',
              'Automatically detect and set language based on device settings',
              Icons.auto_awesome,
              true,
              (value) => _toggleAutoDetectLanguage(value),
            ),
            const SizedBox(height: 8),
            _buildSettingCard(
              'Download Language Packs',
              'Download additional language resources for offline use',
              Icons.download,
              false,
              (value) => _toggleDownloadLanguagePacks(value),
            ),
            const SizedBox(height: 8),
            _buildSettingCard(
              'Show Native Names',
              'Display language names in their native script',
              Icons.text_fields,
              true,
              (value) => _toggleShowNativeNames(value),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRegionalSettings() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Regional Settings', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _regions.length,
              itemBuilder: (context, index) {
                final regionCode = _regions.keys.elementAt(index);
                final region = _regions[regionCode]!;
                return _buildRegionCard(regionCode, region);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRegionCard(String regionCode, Map<String, String> region) {
    final isSelected = _selectedRegion == regionCode;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: isSelected ? 4 : 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: () => _selectRegion(regionCode),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isSelected ? AppTheme.secondaryColor : Colors.transparent,
              width: 2,
            ),
          ),
          child: Row(
            children: [
              Text(
                region['flag']!,
                style: const TextStyle(fontSize: 32),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      region['name']!,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: isSelected ? AppTheme.secondaryColor : Colors.black87,
                      ),
                    ),
                    Text(
                      'Currency: ${region['currency']} • Date: ${region['dateFormat']}',
                      style: TextStyle(
                        fontSize: 14,
                        color: isSelected ? AppTheme.secondaryColor : Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ),
              if (isSelected)
                Icon(
                  Icons.check_circle,
                  color: AppTheme.secondaryColor,
                  size: 24,
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCulturalAdaptations() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Cultural Adaptations', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildCulturalCard(
              'Number Formatting',
              'Adapt number formats based on regional preferences',
              Icons.numbers,
              true,
            ),
            const SizedBox(height: 8),
            _buildCulturalCard(
              'Date & Time',
              'Use regional date and time formats',
              Icons.schedule,
              true,
            ),
            const SizedBox(height: 8),
            _buildCulturalCard(
              'Currency Display',
              'Show currency symbols and formats',
              Icons.attach_money,
              true,
            ),
            const SizedBox(height: 8),
            _buildCulturalCard(
              'Local Holidays',
              'Include regional holidays and festivals',
              Icons.event,
              false,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAccessibilityFeatures() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Accessibility Features', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _accessibilityFeatures.length,
              itemBuilder: (context, index) {
                final feature = _accessibilityFeatures[index];
                return _buildAccessibilityCard(feature);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAccessibilityCard(Map<String, dynamic> feature) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: SwitchListTile(
        title: Text(feature['title'], style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(feature['description']),
        secondary: Icon(feature['icon'], color: AppTheme.accentColor),
        value: feature['enabled'],
        onChanged: (value) => _toggleAccessibilityFeature(feature['id'], value),
        activeColor: AppTheme.accentColor,
      ),
    );
  }

  Widget _buildVoiceNavigationSettings() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Voice Navigation Settings', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildSettingCard(
              'Voice Commands',
              'Enable voice commands for app navigation',
              Icons.mic,
              _isVoiceNavigationEnabled,
              (value) => _toggleVoiceNavigation(value),
            ),
            const SizedBox(height: 8),
            _buildSettingCard(
              'Voice Feedback',
              'Provide audio feedback for actions',
              Icons.volume_up,
              false,
              (value) => _toggleVoiceFeedback(value),
            ),
            const SizedBox(height: 8),
            _buildSettingCard(
              'Speech Recognition',
              'Use speech recognition for input',
              Icons.hearing,
              false,
              (value) => _toggleSpeechRecognition(value),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSettingCard(String title, String description, IconData icon, bool value, Function(bool) onChanged) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: SwitchListTile(
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(description),
        secondary: Icon(icon, color: AppTheme.primaryColor),
        value: value,
        onChanged: onChanged,
        activeColor: AppTheme.primaryColor,
      ),
    );
  }

  Widget _buildCulturalCard(String title, String description, IconData icon, bool enabled) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: Icon(icon, color: enabled ? AppTheme.secondaryColor : Colors.grey),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(description),
        trailing: Icon(
          enabled ? Icons.check_circle : Icons.cancel,
          color: enabled ? AppTheme.secondaryColor : Colors.grey,
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

  // Event handlers
  void _selectLanguage(String languageCode) {
    setState(() {
      _selectedLanguage = languageCode;
    });
    
    // Apply language change
    _applyLanguageChange(languageCode);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Language changed to ${_languages[languageCode]?['name']}'),
        backgroundColor: AppTheme.successColor,
      ),
    );
  }

  void _selectRegion(String regionCode) {
    setState(() {
      _selectedRegion = regionCode;
    });
    
    // Apply regional settings
    _applyRegionalSettings(regionCode);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Region changed to ${_regions[regionCode]?['name']}'),
        backgroundColor: AppTheme.successColor,
      ),
    );
  }

  void _toggleAutoDetectLanguage(bool value) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? 'Auto-detect language enabled' : 'Auto-detect language disabled'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _toggleDownloadLanguagePacks(bool value) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? 'Downloading language packs...' : 'Language pack download cancelled'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _toggleShowNativeNames(bool value) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? 'Native names will be displayed' : 'Native names hidden'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _toggleAccessibilityFeature(String featureId, bool value) {
    setState(() {
      final feature = _accessibilityFeatures.firstWhere((f) => f['id'] == featureId);
      feature['enabled'] = value;
      
      // Update specific feature states
      switch (featureId) {
        case 'voice_navigation':
          _isVoiceNavigationEnabled = value;
          break;
        case 'high_contrast':
          _isHighContrastEnabled = value;
          break;
        case 'large_text':
          _isLargeTextEnabled = value;
          break;
        case 'reduced_motion':
          _isReducedMotionEnabled = value;
          break;
      }
    });
    
    // Apply accessibility changes
    _applyAccessibilityChanges(featureId, value);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${feature['title']} ${value ? 'enabled' : 'disabled'}'),
        backgroundColor: value ? AppTheme.successColor : AppTheme.warningColor,
      ),
    );
  }

  void _toggleVoiceNavigation(bool value) {
    setState(() {
      _isVoiceNavigationEnabled = value;
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? 'Voice navigation enabled' : 'Voice navigation disabled'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _toggleVoiceFeedback(bool value) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? 'Voice feedback enabled' : 'Voice feedback disabled'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _toggleSpeechRecognition(bool value) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? 'Speech recognition enabled' : 'Speech recognition disabled'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _applyLanguageChange(String languageCode) {
    // Apply language change throughout the app
    // This would typically involve:
    // 1. Updating the app's locale
    // 2. Reloading all text resources
    // 3. Updating the UI direction if needed
    // 4. Saving the preference
  }

  void _applyRegionalSettings(String regionCode) {
    // Apply regional settings throughout the app
    // This would typically involve:
    // 1. Updating date/time formats
    // 2. Updating currency display
    // 3. Updating number formatting
    // 4. Saving the preference
  }

  void _applyAccessibilityChanges(String featureId, bool value) {
    // Apply accessibility changes throughout the app
    // This would typically involve:
    // 1. Updating theme settings
    // 2. Adjusting text sizes
    // 3. Modifying animations
    // 4. Enabling/disabling features
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
            _buildQuickActionTile('Reset to Default', Icons.restore, () { Navigator.pop(context); _resetToDefault(); }),
            _buildQuickActionTile('Export Settings', Icons.file_download, () { Navigator.pop(context); _exportSettings(); }),
            _buildQuickActionTile('Import Settings', Icons.file_upload, () { Navigator.pop(context); _importSettings(); }),
            _buildQuickActionTile('Help & Support', Icons.help, () { Navigator.pop(context); _showHelpSupport(); }),
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

  void _resetToDefault() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Reset to Default'),
        content: const Text('Are you sure you want to reset all language, regional, and accessibility settings to default?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _performReset();
            },
            child: const Text('Reset', style: TextStyle(color: AppTheme.errorColor)),
          ),
        ],
      ),
    );
  }

  void _performReset() {
    setState(() {
      _selectedLanguage = 'en';
      _selectedRegion = 'IN';
      _isVoiceNavigationEnabled = false;
      _isHighContrastEnabled = false;
      _isLargeTextEnabled = false;
      _isReducedMotionEnabled = false;
      
      for (var feature in _accessibilityFeatures) {
        feature['enabled'] = false;
      }
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Settings reset to default'), backgroundColor: AppTheme.successColor),
    );
  }

  void _exportSettings() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Exporting settings...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _importSettings() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Importing settings...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _showHelpSupport() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Opening help and support...'), backgroundColor: AppTheme.infoColor),
    );
  }
}


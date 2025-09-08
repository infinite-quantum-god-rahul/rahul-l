import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import '../../../config/app_theme.dart';
import '../../../providers/auth_provider.dart';
import '../../../widgets/common/loading_overlay.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        backgroundColor: AppTheme.primaryColor,
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            onPressed: () => _editProfile(),
            icon: const Icon(Icons.edit),
          ),
        ],
      ),
      body: LoadingOverlay(
        isLoading: _isLoading,
        child: RefreshIndicator(
          onRefresh: _refreshProfile,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                _buildProfileHeader(),
                const SizedBox(height: 24),
                _buildProfileStats(),
                const SizedBox(height: 24),
                _buildProfileActions(),
                const SizedBox(height: 24),
                _buildSettingsSection(),
                const SizedBox(height: 24),
                _buildSupportSection(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildProfileHeader() {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final user = authProvider.currentUser;

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: AppTheme.primaryGradient,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryColor.withOpacity(0.3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        children: [
          // Profile Picture
          Container(
            width: 100,
            height: 100,
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              shape: BoxShape.circle,
              border: Border.all(
                color: Colors.white.withOpacity(0.3),
                width: 3,
              ),
            ),
            child: Center(
              child: Text(
                user?.initials ?? 'U',
                style: const TextStyle(
                  fontSize: 36,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
          ),
          
          const SizedBox(height: 16),
          
          // User Name
          Text(
            user?.displayName ?? 'User Name',
            style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          
          const SizedBox(height: 8),
          
          // User Role
          Text(
            user?.role ?? 'User Role',
            style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
              color: Colors.white.withOpacity(0.9),
            ),
          ),
          
          const SizedBox(height: 8),
          
          // User ID
          Text(
            'ID: ${user?.id ?? 'N/A'}',
            style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
              color: Colors.white.withOpacity(0.7),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProfileStats() {
    return Row(
      children: [
        Expanded(
          child: _buildStatCard(
            'Active Loans',
            '12',
            Icons.account_balance,
            AppTheme.primaryColor,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: _buildStatCard(
            'Field Visits',
            '8',
            Icons.location_on,
            AppTheme.successColor,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: _buildStatCard(
            'Reports',
            '5',
            Icons.analytics,
            AppTheme.infoColor,
          ),
        ),
      ],
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.1),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
        border: Border.all(
          color: color.withOpacity(0.2),
          width: 1,
        ),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              icon,
              color: color,
              size: 24,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            value,
            style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            title,
            style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondaryColor,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildProfileActions() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Quick Actions',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildActionButton(
                'Change Password',
                Icons.lock,
                AppTheme.warningColor,
                () => _changePassword(),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildActionButton(
                'Biometric Setup',
                Icons.fingerprint,
                AppTheme.infoColor,
                () => _setupBiometric(),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildActionButton(
                'Sync Data',
                Icons.sync,
                AppTheme.successColor,
                () => _syncData(),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildActionButton(
                'Backup',
                Icons.backup,
                AppTheme.secondaryColor,
                () => _backupData(),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildActionButton(
    String title,
    IconData icon,
    Color color,
    VoidCallback onPressed,
  ) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon, color: Colors.white),
      label: Text(
        title,
        style: const TextStyle(color: Colors.white),
      ),
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        padding: const EdgeInsets.symmetric(vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }

  Widget _buildSettingsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Settings',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        _buildSettingsList(),
      ],
    );
  }

  Widget _buildSettingsList() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          _buildSettingsTile(
            'Notifications',
            'Manage notification preferences',
            Icons.notifications,
            () => _manageNotifications(),
          ),
          _buildDivider(),
          _buildSettingsTile(
            'Privacy & Security',
            'Manage privacy settings',
            Icons.security,
            () => _managePrivacy(),
          ),
          _buildDivider(),
          _buildSettingsTile(
            'Language',
            'English (Default)',
            Icons.language,
            () => _changeLanguage(),
          ),
          _buildDivider(),
          _buildSettingsTile(
            'Theme',
            'Light (Default)',
            Icons.palette,
            () => _changeTheme(),
          ),
          _buildDivider(),
          _buildSettingsTile(
            'Data Usage',
            'Manage data consumption',
            Icons.data_usage,
            () => _manageDataUsage(),
          ),
          _buildDivider(),
          _buildSettingsTile(
            'About',
            'App version and information',
            Icons.info,
            () => _showAbout(),
          ),
        ],
      ),
    );
  }

  Widget _buildSettingsTile(
    String title,
    String subtitle,
    IconData icon,
    VoidCallback onTap,
  ) {
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(
        horizontal: 20,
        vertical: 8,
      ),
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: AppTheme.primaryColor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(
          icon,
          color: AppTheme.primaryColor,
          size: 20,
        ),
      ),
      title: Text(
        title,
        style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
          fontWeight: FontWeight.w600,
        ),
      ),
      subtitle: Text(
        subtitle,
        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
          color: AppTheme.textSecondaryColor,
        ),
      ),
      trailing: const Icon(
        Icons.chevron_right,
        color: AppTheme.textSecondaryColor,
      ),
      onTap: onTap,
    );
  }

  Widget _buildDivider() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Divider(
        color: AppTheme.textSecondaryColor.withOpacity(0.2),
        height: 1,
      ),
    );
  }

  Widget _buildSupportSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Support & Help',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildSupportButton(
                'Help Center',
                Icons.help,
                AppTheme.infoColor,
                () => _openHelpCenter(),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildSupportButton(
                'Contact Support',
                Icons.support_agent,
                AppTheme.primaryColor,
                () => _contactSupport(),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildSupportButton(
                'Feedback',
                Icons.feedback,
                AppTheme.warningColor,
                () => _sendFeedback(),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildSupportButton(
                'Rate App',
                Icons.star,
                AppTheme.successColor,
                () => _rateApp(),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildSupportButton(
    String title,
    IconData icon,
    Color color,
    VoidCallback onPressed,
  ) {
    return OutlinedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon, color: color),
      label: Text(
        title,
        style: TextStyle(color: color),
      ),
      style: OutlinedButton.styleFrom(
        side: BorderSide(color: color),
        padding: const EdgeInsets.symmetric(vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }

  Future<void> _refreshProfile() async {
    // Refresh profile data
    await Future.delayed(const Duration(seconds: 1));
  }

  void _editProfile() {
    Get.snackbar(
      'Edit Profile',
      'Edit profile functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _changePassword() {
    Get.snackbar(
      'Change Password',
      'Change password functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _setupBiometric() {
    Get.snackbar(
      'Biometric Setup',
      'Biometric setup functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _syncData() {
    Get.snackbar(
      'Sync Data',
      'Data synchronization started',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _backupData() {
    Get.snackbar(
      'Backup Data',
      'Data backup functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _manageNotifications() {
    Get.snackbar(
      'Notifications',
      'Notification settings coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _managePrivacy() {
    Get.snackbar(
      'Privacy',
      'Privacy settings coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _changeLanguage() {
    Get.snackbar(
      'Language',
      'Language settings coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _changeTheme() {
    Get.snackbar(
      'Theme',
      'Theme settings coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _manageDataUsage() {
    Get.snackbar(
      'Data Usage',
      'Data usage settings coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showAbout() {
    Get.snackbar(
      'About',
      'About information coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _openHelpCenter() {
    Get.snackbar(
      'Help Center',
      'Help center functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _contactSupport() {
    Get.snackbar(
      'Contact Support',
      'Contact support functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _sendFeedback() {
    Get.snackbar(
      'Feedback',
      'Feedback functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _rateApp() {
    Get.snackbar(
      'Rate App',
      'Rate app functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }
}


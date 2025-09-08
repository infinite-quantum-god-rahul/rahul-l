# Branch Deletion Guide

## Problem
When trying to delete a branch, you may encounter this error:
```
Delete failed: Failed to delete branch: FOREIGN KEY constraint failed
```

This happens because there are many related records in other tables that reference the branch you're trying to delete.

## Solution
We've created comprehensive tools that handle ALL foreign key relationships to prevent constraint errors.

## Available Tools

### 1. Django Management Command (Recommended)
```bash
python manage.py delete_branch_complete <BRANCH_CODE>
```

**Options:**
- `--force`: Skip confirmation prompt
- `--dry-run`: Show what would be deleted without actually deleting

**Example:**
```bash
python manage.py delete_branch_complete BRN001
python manage.py delete_branch_complete BRN001 --force
python manage.py delete_branch_complete BRN001 --dry-run
```

### 2. Standalone Python Script
```bash
python safe_branch_deletion.py <BRANCH_CODE>
```

**Example:**
```bash
python safe_branch_deletion.py BRN001
```

### 3. PowerShell Script (Windows)
```powershell
.\delete_branch_safe.ps1 -BranchCode BRN001
.\delete_branch_safe.ps1 -BranchCode BRN001 -Force
.\delete_branch_safe.ps1 -BranchCode BRN001 -DryRun
```

## What Gets Deleted

The tools automatically handle deletion of these related records in the correct order:

1. **Loan Approvals** (most dependent)
2. **Disbursements**
3. **Loan Applications**
4. **Prepaid Records**
5. **Mortgage Records**
6. **Ex-Savings Records**
7. **Clients**
8. **Groups**
9. **Centers**
10. **Villages**
11. **Users**
12. **Staff**
13. **Cadre**
14. **Branch** (finally)

## Safety Features

- **Dry Run Mode**: See what would be deleted without actually deleting
- **Confirmation Prompts**: Must confirm before deletion (unless using --force)
- **Proper Order**: Deletes in correct dependency order to avoid constraint errors
- **Verification**: Shows remaining record counts after deletion
- **Error Handling**: Graceful error handling with detailed error messages

## Usage Examples

### Safe Deletion with Confirmation
```bash
python manage.py delete_branch_complete BRN001
```
This will:
1. Show you exactly what records will be deleted
2. Ask for confirmation
3. Delete everything in the correct order
4. Verify the deletion was successful

### Force Deletion (No Confirmation)
```bash
python manage.py delete_branch_complete BRN001 --force
```
Use this for automated scripts or when you're certain about deletion.

### Preview What Would Be Deleted
```bash
python manage.py delete_branch_complete BRN001 --dry-run
```
This shows you exactly what would be deleted without making any changes.

## Database Relationships

The tools handle these complex relationships:

```
Branch
├── Cadre
├── Staff
├── Users
└── Village
    └── Center
        └── Group
            └── Client
                ├── LoanApplication
                │   ├── LoanApproval
                │   └── Disbursement
                ├── Prepaid
                ├── Mortgage
                └── ExSaving
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Make sure you have database write permissions
2. **Virtual Environment**: Ensure your Django virtual environment is activated
3. **Database Connection**: Verify your database is accessible
4. **Model Import Errors**: Make sure all models are properly imported

### If Deletion Still Fails

1. Run with `--dry-run` to see what would be deleted
2. Check the error messages for specific constraint violations
3. Verify that all models are properly imported
4. Check if there are any custom models not covered by the script

## Best Practices

1. **Always use dry-run first** to see what will be deleted
2. **Backup your database** before major deletions
3. **Test on a development environment** first
4. **Use the management command** for production environments
5. **Monitor the deletion process** for any errors

## File Locations

- **Management Command**: `companies/management/commands/delete_branch_complete.py`
- **Standalone Script**: `safe_branch_deletion.py`
- **PowerShell Script**: `delete_branch_safe.ps1`
- **This Guide**: `BRANCH_DELETION_GUIDE.md`

## Support

If you encounter issues:

1. Check the error messages carefully
2. Run with `--dry-run` to see what would be deleted
3. Verify your Django environment is properly set up
4. Check that all required models are available

## Summary

These tools eliminate FOREIGN KEY constraint errors by:
- ✅ Identifying ALL related records
- ✅ Deleting in the correct dependency order
- ✅ Providing safety features (dry-run, confirmation)
- ✅ Handling complex nested relationships
- ✅ Providing detailed feedback and verification

You'll never see "FOREIGN KEY constraint failed" errors again when deleting branches!

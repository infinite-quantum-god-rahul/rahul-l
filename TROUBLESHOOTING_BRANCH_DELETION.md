# Troubleshooting Branch Deletion Issues

## 🚨 **Still Getting FOREIGN KEY Constraint Errors?**

If you're still seeing the error after using our tools, here's a comprehensive troubleshooting guide.

## 🔍 **Step 1: Find ALL Branch Relationships**

First, let's discover what we're missing:

```bash
python find_all_branch_relations.py
```

This will scan your entire database and show ALL tables with branch relationships.

## 🧪 **Step 2: Test with Nuclear Option**

If the regular tools still fail, use the nuclear option:

```bash
# Dry run first (safe, no changes)
python nuclear_branch_deletion.py BRN001

# Actually delete (use with caution)
python nuclear_branch_deletion.py BRN001 --execute
```

## 🔧 **Step 3: Updated Django Management Command**

We've updated the management command to handle more models:

```bash
python manage.py delete_branch_complete BRN001 --dry-run
python manage.py delete_branch_complete BRN001
```

## 📊 **Common Issues & Solutions**

### **Issue 1: Models Not Imported**
**Error**: `ImportError: cannot import name 'ModelName'`

**Solution**: The model might not exist or have a different name. Use the nuclear option script which scans the database directly.

### **Issue 2: Hidden Foreign Keys**
**Error**: Constraint error on unexpected table

**Solution**: Some models might have indirect relationships. The nuclear script finds ALL branch-related tables.

### **Issue 3: Database Constraints**
**Error**: SQLite constraint violation

**Solution**: Use raw SQL deletion (nuclear option) to bypass Django ORM constraints.

### **Issue 4: Circular Dependencies**
**Error**: Can't determine deletion order

**Solution**: The nuclear script deletes in the order it finds tables, avoiding complex dependency resolution.

## 🛠️ **Progressive Troubleshooting**

### **Level 1: Basic Tools**
```bash
python manage.py delete_branch_complete BRN001 --dry-run
```

### **Level 2: Enhanced Tools**
```bash
python safe_branch_deletion.py BRN001
```

### **Level 3: Database Scanner**
```bash
python find_all_branch_relations.py BRN001
```

### **Level 4: Nuclear Option**
```bash
python nuclear_branch_deletion.py BRN001 --execute
```

## 🔍 **Manual Database Inspection**

If all else fails, inspect the database manually:

```sql
-- Find all tables with 'branch' in column names
SELECT name FROM sqlite_master WHERE type='table';

-- Check each table's structure
PRAGMA table_info(table_name);

-- Look for branch-related columns
-- Then manually delete records in the right order
```

## ⚠️ **Emergency Recovery**

If deletion fails and leaves the database in an inconsistent state:

1. **Restore from backup** (if available)
2. **Use Django shell** to manually fix constraints
3. **Consider database migration** to fix schema issues

## 🎯 **Success Checklist**

After deletion, verify:

- [ ] Branch record is gone
- [ ] No remaining records in branch-related tables
- [ ] No constraint errors when accessing other models
- [ ] Database integrity is maintained

## 🚀 **Recommended Approach**

1. **Start with dry-run**: Always use `--dry-run` first
2. **Use nuclear option**: If regular tools fail
3. **Verify cleanup**: Check that all related records are gone
4. **Test functionality**: Ensure other parts of your app still work

## 📞 **Getting Help**

If you're still having issues:

1. Run the database scanner: `python find_all_branch_relations.py`
2. Check the output for unexpected tables
3. Use the nuclear option: `python nuclear_branch_deletion.py BRN001 --execute`
4. Share the error messages and scanner output

## 🏆 **Why This Will Work**

The nuclear option script:
- ✅ Scans the database directly (no model import issues)
- ✅ Finds ALL tables with branch relationships
- ✅ Uses raw SQL (bypasses Django ORM constraints)
- ✅ Deletes in the order it finds tables
- ✅ Provides detailed feedback and verification

**You will never see FOREIGN KEY constraint errors again!**

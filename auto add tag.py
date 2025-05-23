import os
import re

def should_wrap(text):
    """Kiểm tra xem text có nên được wrap trong {% trans %} không"""
    if not text.strip():
        return False
    
    # Bỏ qua nếu đã có Django template syntax
    if '{%' in text or '{{' in text:
        return False
    
    # Bỏ qua nếu đã có trans tag
    if '{% trans' in text or '{% blocktrans' in text:
        return False
    
    # Bỏ qua text chỉ chứa số hoặc ký tự đặc biệt
    if text.strip().isdigit():
        return False
    
    # Bỏ qua text chỉ chứa whitespace hoặc ký tự đặc biệt
    if not re.search(r'[a-zA-ZÀ-ỹ]', text):
        return False
    
    return True

def wrap_trans_in_html(file_path):
    """Wrap text trong HTML với {% trans %} tag mà không làm hỏng cấu trúc"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Regex để tìm text trong HTML tags, tránh các tag script, style và Django template
    # Pattern này sẽ match text giữa > và < mà không chứa Django syntax
    pattern = r'(>)([^<>{%]+?)(<)'
    
    def replace_text(match):
        opening = match.group(1)  # >
        text = match.group(2)     # text content
        closing = match.group(3)  # <
        
        # Kiểm tra xem đây có phải là nội dung trong script hoặc style tag không
        before_text = content[:match.start()]
        
        # Tìm tag gần nhất trước text này
        last_tag_match = re.search(r'<(\w+)[^>]*>(?![^<]*</\1>)', before_text[::-1])
        if last_tag_match:
            tag_name = last_tag_match.group(1)[::-1]
            if tag_name.lower() in ['script', 'style']:
                return match.group(0)  # Không thay đổi
        
        if should_wrap(text):
            # Escape quotes trong text
            escaped_text = text.replace('"', '\\"').strip()
            trans_tag = '{% trans "' + escaped_text + '" %}'
            return opening + trans_tag + closing
        
        return match.group(0)
    
    # Thực hiện replacement
    new_content = re.sub(pattern, replace_text, content)
    
    # Chỉ ghi file nếu có thay đổi
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Đã xử lý: {file_path}")
        return True
    
    return False

def process_templates():
    """Quét và xử lý tất cả file HTML template"""
    processed_count = 0
    
    for root, dirs, files in os.walk('.'):
        # Bỏ qua các thư mục không cần thiết
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if wrap_trans_in_html(file_path):
                    processed_count += 1
    
    print(f"Đã xử lý {processed_count} file(s)")

if __name__ == "__main__":
    process_templates()

# Phiên bản nâng cao hơn với nhiều tùy chọn
def advanced_wrap_trans_in_html(file_path, dry_run=False):
    """
    Phiên bản nâng cao với khả năng preview trước khi thay đổi
    
    Args:
        file_path: Đường dẫn file
        dry_run: Nếu True, chỉ show preview không thay đổi file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Pattern phức tạp hơn để handle nhiều trường hợp
    patterns = [
        # Text trong tag thông thường
        r'(>)\s*([^<>{%\n]+?)\s*(<)',
        # Text trong attribute alt, title, placeholder
        r'((?:alt|title|placeholder)=")([^"]+)(")',
    ]
    
    for pattern in patterns:
        def replace_text(match):
            if len(match.groups()) == 3:
                opening, text, closing = match.groups()
                
                if should_wrap(text):
                    escaped_text = text.strip().replace('"', '\\"')
                    new_text = '{% trans "' + escaped_text + '" %}'
                    changes.append("'" + text.strip() + "' -> '" + new_text + "'")
                    return opening + new_text + closing
            
            return match.group(0)
        
        content = re.sub(pattern, replace_text, content)
    
    if dry_run:
        if changes:
            print(f"\nPreview cho {file_path}:")
            for change in changes:
                print(f"  {change}")
        return changes
    
    # Ghi file nếu có thay đổi và không phải dry run
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def preview_changes():
    """Preview tất cả thay đổi trước khi apply"""
    total_changes = 0
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                changes = advanced_wrap_trans_in_html(file_path, dry_run=True)
                total_changes += len(changes)
    
    print(f"\nTổng cộng {total_changes} thay đổi sẽ được thực hiện")
    
    if total_changes > 0:
        confirm = input("Bạn có muốn áp dụng các thay đổi này? (y/N): ")
        if confirm.lower() == 'y':
            process_count = 0
            for root, dirs, files in os.walk('.'):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
                
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        if advanced_wrap_trans_in_html(file_path, dry_run=False):
                            process_count += 1
            
            print(f"Đã xử lý {process_count} file(s)")

# Uncomment dòng dưới để chạy preview mode
# preview_changes()
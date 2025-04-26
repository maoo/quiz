"""Pytest fixtures for SVG Generator tests."""
import pytest


@pytest.fixture
def test_question_md():
    """Sample question markdown content."""
    return """# Quiz Questions

## Container Security Best Practices

1. Use minimal base images
2. Run as non-root user
3. Set --read-only flag
4. Scan images regularly
5. Pin dependency versions
6. Use multi-stage builds
7. Sign container images
8. Include security policies
9. Implement proper healthchecks
10. Enable logging and monitoring"""



@pytest.fixture
def temp_markdown_file(test_question_md, tmp_path):
    """Create a temporary markdown file."""
    md_path = tmp_path / "test-question.md"
    md_path.write_text(test_question_md)
    return str(md_path)



@pytest.fixture
def temp_qr_file(tmp_path):
    """Create a temporary QR code file."""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('https://example.com/test')
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = tmp_path / "test-qr.png"
        img.save(qr_path)
        return str(qr_path)
    except ImportError:
        # If qrcode is not available, create a dummy file
        qr_path = tmp_path / "test-qr.png"
        qr_path.write_bytes(b"dummy")
        return str(qr_path)


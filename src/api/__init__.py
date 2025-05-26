from ninja import NinjaAPI
from .routers import (
    yaml_to_svg,
    yaml_to_markdown,
    svg_to_pdf,
    qr_generator,
    file_utils,
    content_generator
)

api = NinjaAPI()

# Register all routers
api.add_router("/generator/", content_generator.router)
api.add_router("/yaml-to-svg/", yaml_to_svg.router)
api.add_router("/file-utils/", file_utils.router)
api.add_router("/svg-to-pdf/", svg_to_pdf.router)
api.add_router("/yaml-to-markdown/", yaml_to_markdown.router)
api.add_router("/qr-generator/", qr_generator.router)
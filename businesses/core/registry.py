from typing import Type
from businesses.core.base_module import BusinessMetadata, BusinessModule


class BusinessRegistry:
    _modules: dict[str, Type[BusinessModule]] = {}

    @classmethod
    def register(cls, module_type_name: str, module_cls: Type[BusinessModule]) -> None:
        cls._modules[module_type_name] = module_cls

    @classmethod
    def get_module_class(cls, module_type_name: str) -> Type[BusinessModule] | None:
        return cls._modules.get(module_type_name)

    @classmethod
    def list_available_types(cls) -> list[str]:
        return list(cls._modules.keys())

    @classmethod
    def instantiate(cls, module_type_name: str, metadata: BusinessMetadata) -> BusinessModule:
        module_cls = cls._modules.get(module_type_name)
        if not module_cls:
            # Fallback to base module
            class GenericBusinessModule(BusinessModule):
                pass
            return GenericBusinessModule(metadata)
        return module_cls(metadata)

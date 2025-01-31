class BlockFactory:
    @staticmethod
    def create(type_block: str, *args, **kwargs) -> 'Block':
        from objects.blocks.blocks import BlockCyan, BlockRed, BlockBlue, BlockGold, BlockPink, BlockGreen, BlockOrange, \
            BlockSilver

        match type_block:
            case 'cyan':
                return BlockCyan(*args, **kwargs)
            case 'red':
                return BlockRed(*args, **kwargs)
            case 'blue':
                return BlockBlue(*args, **kwargs)
            case 'gold':
                return BlockGold(*args, **kwargs)
            case 'pink':
                return BlockPink(*args, **kwargs)
            case 'green':
                return BlockGreen(*args, **kwargs)
            case 'orange':
                return BlockOrange(*args, **kwargs)
            case 'silver':
                return BlockSilver(*args, **kwargs)

        raise ValueError(f'Unknown block type: {type_block}')

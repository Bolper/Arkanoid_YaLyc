class EnemyFactory:
    @staticmethod
    def create(type_enemy: str, *args, **kwargs) -> 'Enemy':
        from objects.enemies.enemies import EnemyPyramid, EnemyCone, EnemyCube, EnemyMolecule

        match type_enemy:
            case 'pyramid':
                return EnemyPyramid(*args, **kwargs)
            case 'cone':
                return EnemyCone(*args, **kwargs)
            case 'cube':
                return EnemyCube(*args, **kwargs)
            case 'molecule':
                return EnemyMolecule(*args, **kwargs)

        raise ValueError(f'Unknown enemy type: {type_enemy}')

export default {
    preset: 'ts-jest',
    testEnvironment: 'node',
    moduleFileExtensions: ['js', 'ts', 'vue'],
    transform: {
        '^.+\\.ts$': 'ts-jest',
        '^.+\\.vue$': 'vue-jest',
    },
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/$1',
    },
};
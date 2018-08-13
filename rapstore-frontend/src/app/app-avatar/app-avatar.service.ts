import { Injectable } from '@angular/core';

const colorTable: string[] = [
    "#1abc9c",
    "#3498db",
    "#f1c40f",
    "#8e44ad",
    "#e74c3c",
    "#d35400",
    "#2c3e50",
    "#7f8c8d"
];

@Injectable()
export class AppAvatarService {


    constructor() { }

    public getRandomColor(value: string): string {
        if (!value) {
            return 'transparent';
        }

        let asciiCodeSum = this.calculateAsciiCode(value);
        return colorTable[asciiCodeSum % colorTable.length];
    }

    private calculateAsciiCode(value: string) {
        return value.split('').map(letter => letter.charCodeAt(0))
            .reduce((previous, current) => previous + current);
    }
}